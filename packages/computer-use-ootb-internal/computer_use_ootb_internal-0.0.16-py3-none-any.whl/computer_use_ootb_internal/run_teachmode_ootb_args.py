from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
import argparse
import time
import json
import platform
from typing import Callable
from collections.abc import Callable

from computer_use_ootb_internal.computer_use_demo.executor.teachmode_executor import TeachmodeShowUIExecutor
from computer_use_ootb_internal.computer_use_demo.gui_agent.gui_parser.simple_parser.gui_capture import get_screenshot
from computer_use_ootb_internal.computer_use_demo.gui_agent.llm_utils.oai import encode_image
from computer_use_ootb_internal.computer_use_demo.gui_agent.gui_parser.simple_parser.icon_detection.icon_detection import (
    get_screen_resize_factor,
)
from aws_request import send_request_to_server


# Add these global variables after imports
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add current_task variable to store the running task
current_task = {
    "model": "teach-mode-gpt-4o",
    "task": "task",
    "selected_screen": 0,
    "user_id": "user_id",
    "trace_id": "trace_id",
    "api_keys": None
}


@app.post("/update_params")
async def update_params(params: dict):
    current_task.update(params)
    
    # Start the sampling loop in a new thread
    def run_loop():
        sampling_loop = simple_teachmode_sampling_loop(
            model=current_task["model"],
            task=current_task["task"],
            output_callback=output_callback,
            tool_output_callback=tool_output_callback,
            api_response_callback=api_response_callback,
            selected_screen=current_task["selected_screen"],
            user_id=current_task["user_id"],
            trace_id=current_task["trace_id"],
            api_keys=current_task["api_keys"],
        )

        for step in sampling_loop:
            print(step)
            time.sleep(1)

    thread = threading.Thread(target=run_loop)
    thread.start()
    
    return {"success": True, "message": "Task started", "params": current_task}


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
    Synchronous sampling loop for assistant/tool interactions in 'teach mode'.
    """
    if platform.system() != "Windows":
        raise ValueError("Teach mode is only supported on Windows.")

    executor = TeachmodeShowUIExecutor(
        output_callback=output_callback,
        tool_output_callback=tool_output_callback,
        selected_screen=selected_screen,
    )

    step_count = 0

    if model.startswith("teach-mode"):
        while True:
            # Pause briefly so we don't spam screenshots
            time.sleep(2)

            uia_meta, sc_path = get_screenshot(selected_screen=selected_screen)
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
                "api_keys": api_keys,
            }

            # Send request to inference server
            infer_server_response = send_request_to_server(payload)
            next_plan = infer_server_response["generated_plan"]

            try:
                next_action = json.loads(infer_server_response["generated_action"]["content"])
            except Exception as e:
                print("Error parsing generated_action content:", e)
                continue

            if next_action.get("action") == "STOP":
                final_sc, final_sc_path = get_screenshot(selected_screen=selected_screen)
                output_callback(
                    "No more actions. Task complete. Final State:\n"
                    f"<img src='data:image/png;base64,{encode_image(str(final_sc_path))}'>",
                    sender="bot",
                )
                break

            action_history.append(f"plan: {next_plan} - action: {next_action};")

            for message in executor({"role": "assistant", "content": next_action}, action_history):
                yield message

            step_count += 1

    else:
        raise ValueError("Invalid model selected.")


def output_callback(response: str, sender: str) -> None:
    """
    Callback for text-based output from the assistant.
    """
    pass  


def tool_output_callback(tool_result: str, sender: str) -> None:
    """
    Callback for tool (non-text) output from the assistant.
    """
    pass  


def api_response_callback(response: dict) -> None:
    """
    Callback for receiving API responses.
    """
    pass 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a synchronous sampling loop for assistant/tool interactions in teach-mode."
    )
    parser.add_argument(
        "--model",
        default="teach-mode-gpt-4o",
        help="The model to use for teach-mode (e.g., 'teach-mode-gpt-4o').",
    )
    parser.add_argument(
        "--task",
        # default="Help me to complete the extraction of the viewer data of Downald Trump's first video on youtube,\
        # fill in the excel sheet.",
        # default="Click on the Google Chorme icon",
        default="Help me to complete the extraction of the viewer data of DeepSeek's first video on youtube,\
    fill in the video name and the viewer data to excel sheet.",
        help="The task to be completed by the assistant (e.g., 'Complete some data extraction.').",
    )
    parser.add_argument(
        "--selected_screen",
        type=int,
        default=0,
        help="Index of the screen to capture (default=0).",
    )
    parser.add_argument(
        "--user_id",
        default="liziqi",
        help="User ID for the session (default='liziqi').",
    )
    parser.add_argument(
        "--trace_id",
        default="default_trace",
        help="Trace ID for the session (default='default_trace').",
    )
    parser.add_argument(
        "--api_key_file",
        default="api_key.json",
        help="Path to the JSON file containing API keys (default='api_key.json').",
    )

    args = parser.parse_args()

    # Load API keys

    with open(args.api_key_file, "r") as file:
        current_task["api_keys"] = json.load(file)
    # api_keys = load_from_storage(args.api_key_file)

    print(f"Starting task: {args.task}")

    uvicorn.run(app, host="0.0.0.0", port=7888)

    # Execute the sampling loop
    sampling_loop = simple_teachmode_sampling_loop(
        model=args.model,
        task=args.task,
        output_callback=output_callback,
        tool_output_callback=tool_output_callback,
        api_response_callback=api_response_callback,
        selected_screen=args.selected_screen,
        user_id=args.user_id,
        trace_id=args.trace_id,
        api_keys=current_task["api_keys"],
    )

    # Print each step result
    for step in sampling_loop:
        print(step)
        time.sleep(1)

    print(f"Task '{args.task}' completed. Thanks for using Teachmode-OOTB.")
