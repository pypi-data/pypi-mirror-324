import os
import sys
import io
import time
import json
import platform
from typing import Callable
from collections.abc import Callable

from computer_use_ootb_internal.computer_use_demo.executor.teachmode_executor import TeachmodeShowUIExecutor
from computer_use_ootb_internal.computer_use_demo.gui_agent.gui_parser.simple_parser.gui_capture import get_screenshot
from computer_use_ootb_internal.computer_use_demo.gui_agent.llm_utils.oai import encode_image
from computer_use_ootb_internal.computer_use_demo.gui_agent.gui_parser.simple_parser.icon_detection.icon_detection import get_screen_resize_factor
from aws_request import send_request_to_server


def load_from_storage(file_name):
    with open(file_name, "r") as file:
        return json.load(file)

def simple_teachmode_sampling_loop(
    model: str,
    task: str,
    output_callback: Callable[[str, str], None],
    tool_output_callback: Callable[[str, str], None],
    api_response_callback: Callable[[dict], None],
    api_keys: dict = None,
    action_history: list[dict] = [],
    selected_screen: int = 0,
    user_id: str = None,
    trace_id: str = None,

):
    """
    Synchronous sampling loop for assistant/tool interactions.
    """
    
    print("Checking platform...")
    if platform.system() != "Windows":
        raise ValueError("Teach mode now only supports Windows.")

    
    executor = TeachmodeShowUIExecutor(
            output_callback=output_callback,
            tool_output_callback=tool_output_callback,
            selected_screen=selected_screen
        )
    
    step_count = 0

    if model.startswith("teach-mode"):
        
        model_name = model.replace("teach-mode-", "")
        
        while True:

            time.sleep(2)

            uia_meta, sc_path = get_screenshot(selected_screen=selected_screen)

            print("uia_meta:", uia_meta)

            payload = {
                "uia_data": uia_meta,
                "screenshot_path": sc_path,
                "query": task,
                "action_history": action_history,
                "mode": "teach",
                "user_id": user_id,
                "trace_id": trace_id,
                "scale_factor": get_screen_resize_factor(),  
                "os_name": platform.system(),
                "llm_model": "gpt-4o",
                "api_keys": api_keys
            }
            
            infer_server_response = send_request_to_server(payload)
            print("infer_server_response-", infer_server_response, "-infer_server_response")
            # import pdb; pdb.set_trace()
            
            next_plan = infer_server_response['generated_plan']

            try:
                next_action = json.loads(infer_server_response['generated_action']['content'])
            except Exception as e:
                print("Error parsing generated action:", e)
                import pdb; pdb.set_trace()
                
            if next_action['action'] == "STOP":
                final_sc, final_sc_path = get_screenshot(selected_screen=selected_screen)
                output_callback(
                    f"No more actions. Task complete. Final State:\n<img src='data:image/png;base64,{encode_image(str(final_sc_path))}'>",
                    sender="bot")
                break

            action_history.append(f"plan: {next_plan} - action: {next_action};")

            for message in executor({"role": "assistant", "content": next_action}, action_history):
                yield message
            
            step_count += 1
            
    else:
        raise ValueError("Invalid model selected.")


# Callback placeholders
def output_callback(response, sender):
    # print(f"[output_callback]: {response}")
    pass

def api_response_callback(response, sender):
    # print(f"[api_response_callback]: {response}")

def tool_output_callback(tool_result, sender):
    # print(f"[tool_output_callback]: {tool_result}")
    pass



if __name__ == "__main__":

    time.sleep(2)

    task = "Help me to complete the extraction of the viewer data of Downald Trump's first video on youtube,\
            fill in the excel sheet."

    api_keys = load_from_storage("api_key.json")

    print("Start task:", task)

    sampling_loop = simple_teachmode_sampling_loop(
        model="teach-mode-gpt-4o",
        task=task,
        output_callback=output_callback,
        tool_output_callback=tool_output_callback,
        api_response_callback=api_response_callback,
        selected_screen=0,
        user_id="liziqi",
        trace_id="default_trace",
        api_keys=api_keys,
    )

    for step in sampling_loop:
        print(step)
        time.sleep(1)

    print(f"Task: {task} completed. Thanks for using Teachmode-OOTB.")