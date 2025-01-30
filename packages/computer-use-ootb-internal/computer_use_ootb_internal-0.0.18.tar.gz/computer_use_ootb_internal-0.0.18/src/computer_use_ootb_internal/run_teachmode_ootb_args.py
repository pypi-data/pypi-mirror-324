from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import threading
import argparse
import time
import json
import platform
from typing import Optional, Dict, List
from pathlib import Path

from computer_use_ootb_internal.computer_use_demo.executor.teachmode_executor import TeachmodeShowUIExecutor
from computer_use_ootb_internal.computer_use_demo.gui_agent.gui_parser.simple_parser.gui_capture import get_screenshot
from computer_use_ootb_internal.computer_use_demo.gui_agent.llm_utils.oai import encode_image
from computer_use_ootb_internal.computer_use_demo.gui_agent.gui_parser.simple_parser.icon_detection.icon_detection import (
    get_screen_resize_factor,
)
from computer_use_ootb_internal.aws_request import send_request_to_server

# Pydantic models for request validation
class TaskParams(BaseModel):
    model: str = "teach-mode-gpt-4o"
    task: str
    selected_screen: int = 0
    user_id: str
    trace_id: str
    api_keys: Optional[Dict] = None

# FastAPI app setup
app = FastAPI(title="Teachmode API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global task state
current_task = {
    "model": "teach-mode-gpt-4o",
    "task": "",
    "selected_screen": 0,
    "user_id": "",
    "trace_id": "",
    "api_keys": None
}

@app.post("/update_params")
async def update_params(params: TaskParams):
    try:
        current_task.update(params.dict())
        
        thread = threading.Thread(
            target=run_teachmode_loop,
            args=(current_task,)
        )
        thread.daemon = True
        thread.start()
        
        return {
            "success": True,
            "message": "Task started successfully",
            "params": current_task
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_teachmode_loop(task_params: dict):
    sampling_loop = simple_teachmode_sampling_loop(
        model=task_params["model"],
        task=task_params["task"],
        output_callback=output_callback,
        tool_output_callback=tool_output_callback,
        api_response_callback=api_response_callback,
        selected_screen=task_params["selected_screen"],
        user_id=task_params["user_id"],
        trace_id=task_params["trace_id"],
        api_keys=task_params["api_keys"],
    )

    for step in sampling_loop:
        print(step)
        time.sleep(1)

def simple_teachmode_sampling_loop(
    model: str,
    task: str,
    output_callback: callable,
    tool_output_callback: callable,
    api_response_callback: callable,
    api_keys: Optional[Dict] = None,
    action_history: List[Dict] = None,
    selected_screen: int = 0,
    user_id: Optional[str] = None,
    trace_id: Optional[str] = None,
):
    """
    Synchronous sampling loop for assistant/tool interactions in teach mode.
    """
    if platform.system() != "Windows":
        raise ValueError("Teach mode is only supported on Windows.")

    if action_history is None:
        action_history = []

    executor = TeachmodeShowUIExecutor(
        output_callback=output_callback,
        tool_output_callback=tool_output_callback,
        selected_screen=selected_screen,
    )

    if not model.startswith("teach-mode"):
        raise ValueError(f"Invalid model selected: {model}")

    while True:
        time.sleep(2)  # Prevent screenshot spam

        try:
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

            response = send_request_to_server(payload)
            next_plan = response["generated_plan"]

            try:
                next_action = json.loads(response["generated_action"]["content"])
            except json.JSONDecodeError as e:
                print(f"Error parsing action content: {e}")
                continue

            if next_action.get("action") == "STOP":
                final_sc, final_sc_path = get_screenshot(selected_screen=selected_screen)
                output_callback(
                    "Task completed. Final State:\n"
                    f"<img src='data:image/png;base64,{encode_image(str(final_sc_path))}'>",
                    sender="bot",
                )
                break

            action_history.append(f"plan: {next_plan} - action: {next_action};")
            
            for message in executor({"role": "assistant", "content": next_action}, action_history):
                yield message

        except Exception as e:
            print(f"Error in sampling loop: {e}")
            yield f"Error occurred: {str(e)}"
            break

def output_callback(response: str, sender: str) -> None:
    """Handle text output from assistant"""
    print(f"{sender}: {response}")

def tool_output_callback(tool_result: str, sender: str) -> None:
    """Handle tool output from assistant"""
    print(f"Tool {sender}: {tool_result}")

def api_response_callback(response: dict) -> None:
    """Handle API responses"""
    print(f"API Response: {response}")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Teachmode-OOTB: Assistant/tool interactions in teach-mode"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7888,
        help="Port to run the FastAPI server on"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to run the FastAPI server on"
    )
    parser.add_argument(
        "--api-key-file",
        type=Path,
        default=Path("api_key.json"),
        help="Path to API keys JSON file"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Load API keys if file exists
    if args.api_key_file.exists():
        try:
            with open(args.api_key_file) as f:
                current_task["api_keys"] = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse API key file: {args.api_key_file}")
    
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()