import requests
import json

from computer_use_ootb_internal.computer_use_demo.gui_agent.planner.teach_mode_vlm_planner import TeachModeVLMPlanner, _message_filter_callback, _maybe_filter_to_n_most_recent_images
from computer_use_ootb_internal.computer_use_demo.gui_agent.llm_utils.oai import encode_image
from computer_use_ootb_internal.computer_use_demo.tools.screen_capture import get_screenshot
from computer_use_ootb_internal.computer_use_demo.gui_agent.llm_utils.llm_utils import extract_data


class RemoteTeachModeVLMPlanner(TeachModeVLMPlanner):
    _NAV_SYSTEM = """You are an assistant trained to navigate the desktop screen. 
    Given a task instruction, a screen observation, and an action history sequence, 
    output the next action and wait for the next observation. 
    Here is the action space:
    {_ACTION_SPACE}
    """
    
    _OOTB_Executor_Action_Space = """
        1. CLICK: Click on an element, value is not applicable and the position [x,y] is required. 
        2. INPUT: Type a string into an element, value is a string to type and the position [x,y] is required. 
        3. SELECT: Select a value for an element, value is not applicable and the position [x,y] is required. 
        4. HOVER: Hover on an element, value is not applicable and the position [x,y] is required.
        5. ANSWER: Answer the question, value is the answer and the position is not applicable.
        6. ENTER: Enter operation, value and position are not applicable.
        7. SCROLL: Scroll the screen, value is the direction to scroll and the position is not applicable.
        8. SELECT_TEXT: Select some text content, value is not applicable and position [[x1,y1], [x2,y2]] is the start and end position of the select operation.
        9. COPY: Copy the text, value is the text to copy and the position is not applicable.
        10. ESC: ESCAPE operation, value and position are not applicable.
        """
    
    
    
    def __init__(
        self,
        remote_api_url: str,  ##
        api_key: str,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.remote_api_url = remote_api_url
        self.api_key = api_key
        self.system_prompt = self._NAV_SYSTEM.format(
            _ACTION_SPACE=self._OOTB_Executor_Action_Space
        )

    def __call__(self, messages: list, screenshot_path: str = None):
        """
        Override the __call__ method to send data to the remote API.
        """
        in_context = self.history_manager.get_in_context_example(self.user_id, self.trace_id)

        # Filter and prepare messages
        planner_messages = _message_filter_callback(messages)

        if self.only_n_most_recent_images:
            _maybe_filter_to_n_most_recent_images(planner_messages, self.only_n_most_recent_images)

        # Take a screenshot if not provided
        if screenshot_path is None:
            _, screenshot_path = get_screenshot(selected_screen=self.selected_screen)

        # Encode the screenshot for sending
        image_base64 = encode_image(screenshot_path)

        # Add in-context example
        self.add_in_context_example(in_context)

        # Prepare the payload for the remote API
        payload = {
            "system_prompt": self.system_prompt,
            "messages": planner_messages,
            "screenshot": image_base64,
            "model": self.model,
            "max_tokens": self.max_tokens,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Send the request to the remote API
        response = requests.post(self.remote_api_url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} from remote API.")
            print(f"Response: {response.text}")
            return None

        # Parse the API response
        response_data = response.json()

        # Extract the plan and token usage
        vlm_response_json = extract_data(response_data.get("vlm_response", ""), "json")
        token_usage = response_data.get("token_usage", 0)

        # Update total token usage and cost
        self.total_token_usage += token_usage
        self.total_cost += (token_usage * 0.15 / 1000000)

        print(f"{self.model} token usage: {token_usage}")
        print(f"VLMPlanner total token usage so far: {self.total_token_usage}. Total cost so far: $USD{self.total_cost:.5f}")

        # Format and display the plan
        vlm_plan_str = ""
        for key, value in json.loads(vlm_response_json).items():
            if key == "Thinking":
                vlm_plan_str += f'{value}'
            else:
                vlm_plan_str += f'\n{key}: {value}'

        return vlm_response_json

    def add_in_context_example(self, in_context_example: str):
        """
        Extend the add_in_context_example method to ensure it is sent to the remote API.
        """
        self.system_prompt += f"""NOTE: Reference the following action trajectory to do the task, when user ask you to do the similar task.    
IN-CONTEXT EXAMPLE:
{in_context_example}
"""

# Example usage
if __name__ == "__main__":
    remote_planner = RemoteTeachModeVLMPlanner(
        remote_api_url="https://example.com/api/vlm_planner",
        api_key="your_api_key_here",
        model="your_model_here",
        system_prompt_suffix="Custom prompt suffix here",
        output_callback=print,
        api_response_callback=print,
        user_id="user123",
        trace_id="trace123",
    )

    messages = [
        {"role": "user", "content": "Open the settings menu."}
    ]

    remote_planner(messages)
