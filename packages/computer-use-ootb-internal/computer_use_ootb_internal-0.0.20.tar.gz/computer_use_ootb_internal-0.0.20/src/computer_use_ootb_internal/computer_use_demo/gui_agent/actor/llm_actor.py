import os
import ast
import base64
from io import BytesIO
from pathlib import Path
from uuid import uuid4
import datetime

import platform
import pyautogui
import requests
import torch
from PIL import Image, ImageDraw
from qwen_vl_utils import process_vision_info
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration

from computer_use_ootb_internal.computer_use_demo.gui_agent.llm_utils.oai import encode_image
from computer_use_ootb_internal.computer_use_demo.tools.colorful_text import colorful_text_showui, colorful_text_vlm

from transformers import AutoModelForCausalLM, AutoTokenizer

from ..llm_utils.run_litellm import run_litellm
import json
os.environ["TOKENIZERS_PARALLELISM"] = "false"


class LLMActor:
    def __init__(self, llm_model, output_callback, device=torch.device("cpu"), local=True):
        self.device = device
        # self.split = split
        self.output_callback = output_callback
        self.os_name = platform.system()

        if llm_model in ["qwen2.5"]:
            # load local model
            model_name = "Qwen/Qwen2.5-7B-Instruct"
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype="auto",
                device_map="auto"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        elif llm_model in ['gpt-4o', 'gpt-4o-mini']:
            # do nothing
            self.model = llm_model

        self.action_history = ''  # Initialize action history

    def __call__(self, messages, parsed_gui, screenshot_path):

        task = messages
        formatted_gui = self.format_parsed_gui(parsed_gui)
        prompt_message = self.get_prompt(formatted_gui, task)
        system_prompt = self.get_system_prompt()

        # Call llm to get the next action
        response = run_litellm(
            messages=prompt_message, 
            system=system_prompt, 
            llm=self.model
        )

        # TODO: uncomment this for support gradio image display
        image_base64 = encode_image(screenshot_path)
        # self.output_callback(f'Screenshot for {colorful_text_showui}:\n<img src="data:image/png;base64,{image_base64}">', sender="bot")
        print("response:", response)
        # Update action history
        result = response[0]
        
        self.action_history += result + '\n'
        # 从response中提取json内容

        
        # Return response in expected format
        response = {'content': result, 'role': 'assistant'}
        return response

    def parse_showui_output(self, output_text):
        try:
            # Ensure the output is stripped of any extra spaces
            output_text = output_text.strip()

            # Wrap the input in brackets if it looks like a single dictionary
            if output_text.startswith("{") and output_text.endswith("}"):
                output_text = f"[{output_text}]"

            # Validate if the output resembles a list of dictionaries
            if not (output_text.startswith("[") and output_text.endswith("]")):
                raise ValueError("Output does not look like a valid list or dictionary.")

            # Parse the output using ast.literal_eval
            parsed_output = ast.literal_eval(output_text)

            # Ensure the result is a list
            if isinstance(parsed_output, dict):
                parsed_output = [parsed_output]
            elif not isinstance(parsed_output, list):
                raise ValueError("Parsed output is neither a dictionary nor a list.")

            # Ensure all elements in the list are dictionaries
            if not all(isinstance(item, dict) for item in parsed_output):
                raise ValueError("Not all items in the parsed output are dictionaries.")

            return parsed_output

        except Exception as e:
            print(f"Error parsing output: {e}")
            return None

    
    @staticmethod
    def format_parsed_gui(gui_data):
        result = []
        # Loop through the 'teach_mode_GUI' list
        for section_name, section in gui_data.items():
            for panel in section:
                elements = panel.get('elements', [[]])
                for group in elements:
                    row_result = []  # Collect items row-wise
                    for item in group:
                        name = item.get('name', '')
                        rectangle = item.get('rectangle', [])
                        # Calculate the midpoint of the bounding box
                        x1, y1, x2, y2 = map(int, rectangle)
                        mid_x = (x1 + x2) // 2
                        mid_y = (y1 + y2) // 2
                        row_result.append(f"{name} [{mid_x}, {mid_y}]")
                    result.append('; '.join(row_result))  # Join row items with semicolon
        
        # Join all formatted rows into a single string
        return '\n'.join(result)

    def get_prompt(self, formatted_gui, task):
        return f"""The information shown in the screenshot is:
{formatted_gui}


What you need to do is:
{task}

Output the next action in the following format:
```json
{{"action": "ACTION_TYPE", "text": "text_to_type", "coordinate": [x,y]}}
```

Let's do it:
"""

    def get_system_prompt(self):
        DATETIME = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"""System Overview:
You have access to a set of functions that allow you to interact with a computing environment. 

String and scalar parameters should be passed as is. Lists and objects should be passed in JSON format.
You can respond to the user based on the results or make further function calls.

Available Functions:

Computer Interaction (GUI):
- Description: 
    Use a mouse and keyboard to interact with the computer and take screenshots.
    You can only interact with the desktop GUI (no terminal or application menu access).
- Actions include:
    - key: Press a key or key-combination.
    - type: Type a string of text.
    - mouse_move: Move the cursor to specified coordinates.
    - left_click, right_click, middle_click, double_click: Perform mouse clicks.
    - left_click_drag: Click and drag the cursor.
    - get_statistics_info: Get the statistical information when it is shown in the screenshot and user wants to know.
- Parameters:
    - action (required): The action to perform, such as key, type, mouse_move, etc.
    - coordinate: The (x, y) coordinates for mouse-related actions.
    - text: The text to type or key to press for type and key actions.

System Capabilities:
You are using an {self.os_name} system.
The current date is [{DATETIME}].
"""




if __name__ == "__main__":
    # Initialize the actor
    actor = ShowUIActor(
        model_path="",
        device=torch.device("mps"),
        split='web',
    )

    # Define the task
    task = "Search for 'weather for New York city'."

    # Initialize messages
    messages = [{"role": "user", "content": task}]

    # Simulate multiple interactions
    for _ in range(3):  # Adjust the range as needed
        # Call the actor
        response = actor(messages)
        # Print the response
        print("Response from actor:", response)
        # Add assistant's response to messages
        messages.append(response)
