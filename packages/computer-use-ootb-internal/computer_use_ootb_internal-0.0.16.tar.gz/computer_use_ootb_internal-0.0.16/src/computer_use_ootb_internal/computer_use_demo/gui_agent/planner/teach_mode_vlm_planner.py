import json
import asyncio
import platform
from collections.abc import Callable
from datetime import datetime
from enum import StrEnum
from typing import Any, cast, Dict, Callable

from anthropic import APIResponse
from anthropic.types import TextBlock, ToolResultBlockParam
from anthropic.types.beta import BetaMessage, BetaTextBlock, BetaToolUseBlock, BetaMessageParam

from computer_use_ootb_internal.computer_use_demo.tools.screen_capture import get_screenshot
from computer_use_ootb_internal.computer_use_demo.gui_agent.llm_utils.run_litellm import run_litellm
from computer_use_ootb_internal.computer_use_demo.gui_agent.llm_utils.oai import run_oai_interleaved, encode_image
from computer_use_ootb_internal.computer_use_demo.gui_agent.llm_utils.qwen import run_qwen
from computer_use_ootb_internal.computer_use_demo.gui_agent.llm_utils.llm_utils import extract_data
from computer_use_ootb_internal.computer_use_demo.tools.colorful_text import colorful_text_showui, colorful_text_vlm

import torch
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info

from computer_use_ootb_internal.computer_use_demo.history.history_manager import HistoryManager

def split_button_reference(text):
    import re
    # Define the regex pattern to match <button_reference: ... >
    pattern = r"<button_reference:([^>]+)>"

    # Split the text based on the pattern and capture the path
    parts = re.split(pattern, text)

    # Create the final list with cleaned paths
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # Captured group (the path inside button_reference)
            result.append(part)
        elif part.strip():
            result.append(part)

    return result

class TeachModeVLMPlanner:
    def __init__(
        self,
        model: str, 
        # provider: str, 
        system_prompt_suffix: str, 
        # api_key: str,
        output_callback: Callable, 
        api_response_callback: Callable,
        user_id: str,
        trace_id: str,
        max_tokens: int = 4096,
        only_n_most_recent_images: int | None = None,
        selected_screen: int = 0,
        print_usage: bool = True,
        device: torch.device = torch.device("cpu"),
    ):
        self.device = device
        self.model = model
        
        # self.provider = provider
        # self.api_key = api_key
        self.system_prompt_suffix = system_prompt_suffix

        self.api_response_callback = api_response_callback
        self.max_tokens = max_tokens
        self.only_n_most_recent_images = only_n_most_recent_images
        self.selected_screen = selected_screen
        self.output_callback = output_callback
        self.system_prompt = self._get_system_prompt() + self.system_prompt_suffix

        self.print_usage = print_usage
        self.total_token_usage = 0
        self.total_cost = 0

        self.user_id = user_id
        self.trace_id = trace_id

        self.history_manager = HistoryManager()


    def __call__(self, messages: list, screenshot_path: str=None):
        in_context = self.history_manager.get_in_context_example(self.user_id, self.trace_id)
        
        # drop looping actions msg, byte image etc
        # TODO: why not use the message filter as the loop?
        planner_messages = _message_filter_callback(messages)  
        print(f"filtered_messages: {planner_messages}")

        if self.only_n_most_recent_images:
            _maybe_filter_to_n_most_recent_images(planner_messages, self.only_n_most_recent_images)

        # Take a screenshot
        if screenshot_path is None:
            _, screenshot_path = get_screenshot(selected_screen=self.selected_screen)

        # Display screenshot in gradio
        image_base64 = encode_image(screenshot_path)
        self.output_callback(f'Screenshot for {colorful_text_vlm}:\n<img src="data:image/png;base64,{image_base64}">',
                             sender="bot")
        

        # Add in-context example
        self.add_in_context_example(in_context)
    
        if isinstance(planner_messages[-1], dict):
            if not isinstance(planner_messages[-1]["content"], list):
                planner_messages[-1]["content"] = [planner_messages[-1]["content"]]
            planner_messages[-1]["content"].append(screenshot_path)

        print(f"Sending messages to VLMPlanner: {planner_messages}")
        print(f"Sending messages to VLMPlanner: {self.system_prompt}")

        # Generate response and token usage
        vlm_response, token_usage = run_litellm(
            messages=planner_messages,
            system=self.system_prompt,
            llm=self.model,
            max_tokens=self.max_tokens,
            temperature=0,
        )

        print(f"{self.model} token usage: {token_usage}")
        self.total_token_usage += token_usage
        self.total_cost += (token_usage * 0.15 / 1000000)  # https://openai.com/api/pricing/
            
        print(f"VLMPlanner response: {vlm_response}")
        
        if self.print_usage:
            print(f"VLMPlanner total token usage so far: {self.total_token_usage}. Total cost so far: $USD{self.total_cost:.5f}")
        
        # Extract data
        vlm_response_json = extract_data(vlm_response, "json")

        # vlm_plan_str = '\n'.join([f'{key}: {value}' for key, value in json.loads(response).items()])
        vlm_plan_str = ""
        for key, value in json.loads(vlm_response_json).items():
            if key == "Thinking":
                vlm_plan_str += f'{value}'
            else:
                vlm_plan_str += f'\n{key}: {value}'
        
        self.output_callback(f"{colorful_text_vlm}:\n{vlm_plan_str}", sender="bot")
        
        return vlm_response_json

    def add_in_context_example(self, in_context_example: str):
        self.system_prompt += f"""NOTE: Reference the following action trajectory to do the task, when user ask you to do the similar task.    
IN-CONTEXT EXAMPLE:
{in_context_example}
"""

    def _api_response_callback(self, response: APIResponse):
        self.api_response_callback(response)
        

    def reformat_messages(self, messages: list):
        pass

    def _get_system_prompt(self):
        os_name = platform.system()
        return f"""
You are using an {os_name} device.
You are able to use a mouse and keyboard to interact with the computer based on the given task and screenshot.
You can only interact with the desktop GUI (no terminal or application menu access).

You may be given some history plan and actions, this is the response from the previous loop.
You should carefully consider your plan base on the task, screenshot, and history actions.

Your available "Next Action" only include:
- ENTER: Press an enter key.
- ESCAPE: Press an ESCAPE key.
- INPUT: Input a string of text.
- CLICK: Describe the ui element to be clicked.
- HOVER: Describe the ui element to be hovered.
- SCROLL: Scroll the screen, you must specify up or down.
- PRESS: Describe the ui element to be pressed.


Output format:
```json
{{
    "Thinking": str, # describe your thoughts on how to achieve the task, choose one action from available actions at a time.
    "Next Action": str, "action_type, action description" | "None" # one action at a time, describe it in short and precisely. 
}}
```

One Example:
```json
{{  
    "Thinking": "I need to search and navigate to amazon.com.",
    "Next Action": "CLICK 'Search Google button' <button_reference:icon_0004.png>."
}}
```

IMPORTANT NOTES:
0. Carefully observe the screenshot and read history actions.
1. You should only give a single action at a time. for example, INPUT text, and ENTER can't be in one Next Action.
2. Attach the text to Next Action, if there is text or any description for the button. 
3. You can provide the reference of the button, such as "<button_reference:icon_0004.png>", if you can find it in the in-context example.
4. You should not include other actions, such as keyboard shortcuts.
5. When the task is completed, you should say "Next Action": "None" in the json field.
""" 

    

def _maybe_filter_to_n_most_recent_images(
    messages: list[BetaMessageParam],
    images_to_keep: int,
    min_removal_threshold: int = 10,
):
    """
    With the assumption that images are screenshots that are of diminishing value as
    the conversation progresses, remove all but the final `images_to_keep` tool_result
    images in place, with a chunk of min_removal_threshold to reduce the amount we
    break the implicit prompt cache.
    """
    if images_to_keep is None:
        return messages

    tool_result_blocks = cast(
        list[ToolResultBlockParam],
        [
            item
            for message in messages
            for item in (
                message["content"] if isinstance(message["content"], list) else []
            )
            if isinstance(item, dict) and item.get("type") == "tool_result"
        ],
    )

    total_images = sum(
        1
        for tool_result in tool_result_blocks
        for content in tool_result.get("content", [])
        if isinstance(content, dict) and content.get("type") == "image"
    )

    images_to_remove = total_images - images_to_keep
    # for better cache behavior, we want to remove in chunks
    images_to_remove -= images_to_remove % min_removal_threshold

    for tool_result in tool_result_blocks:
        if isinstance(tool_result.get("content"), list):
            new_content = []
            for content in tool_result.get("content", []):
                if isinstance(content, dict) and content.get("type") == "image":
                    if images_to_remove > 0:
                        images_to_remove -= 1
                        continue
                new_content.append(content)
            tool_result["content"] = new_content


def _message_filter_callback(messages: list):
    """
    Filter messages to keep only user messages and convert them to strings.
    """
    filtered_list = []
    try:
        for msg in messages:
            if msg.get('role') in ['user']:
                if not isinstance(msg["content"], list):
                    msg["content"] = [msg["content"]]
                if isinstance(msg["content"][0], TextBlock):
                    filtered_list.append(str(msg["content"][0].text))  # User message
                elif isinstance(msg["content"][0], str):
                    filtered_list.append(msg["content"][0])  # User message
                else:
                    print("[_message_filter_callback]: drop message", msg)
                    continue
                
            else:
                print("[_message_filter_callback]: drop message", msg)
                continue
            
    except Exception as e:
        print("[_message_filter_callback]: error", e)
                
    return filtered_list