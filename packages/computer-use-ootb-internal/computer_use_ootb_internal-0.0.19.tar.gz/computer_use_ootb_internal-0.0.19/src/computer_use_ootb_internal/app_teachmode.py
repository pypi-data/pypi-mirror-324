import argparse
import time
import json
from typing import Optional, Dict
import gradio as gr
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from screeninfo import get_monitors
import threading
from computer_use_ootb_internal.computer_use_demo.tools.computer import get_screen_details
from computer_use_ootb_internal.run_teachmode_ootb_args import simple_teachmode_sampling_loop

# FastAPI setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request validation
class TaskParams(BaseModel):
    model: str = "teach-mode-gpt-4o"
    task: str
    selected_screen: int = 0
    user_id: str
    trace_id: str
    api_keys: Optional[Dict] = None

# Global state
current_task = {
    "model": "teach-mode-gpt-4o",
    "task": "",
    "selected_screen": 0,
    "user_id": "",
    "trace_id": "",
    "api_keys": None,
    "chatbot_messages": []
}

# Get screen information
screens = get_monitors()
SCREEN_NAMES, SELECTED_SCREEN_INDEX = get_screen_details()

def setup_state(state, args):
    state["model"] = args.model
    state["task"] = args.task
    state["selected_screen"] = args.selected_screen
    state["user_id"] = args.user_id
    state["trace_id"] = args.trace_id
    state["api_keys"] = args.api_keys
    
    if 'chatbot_messages' not in state:
        state['chatbot_messages'] = []

def process_input(user_input, state):
    state['chatbot_messages'].append(gr.ChatMessage(role="user", content=user_input))
    yield state['chatbot_messages']

    sampling_loop = simple_teachmode_sampling_loop(
        model=state["model"],
        task=state["task"],
        selected_screen=state["selected_screen"],
        user_id=state["user_id"],
        trace_id=state["trace_id"],
        api_keys=state["api_keys"],
    )

    for loop_msg in sampling_loop:
        state['chatbot_messages'].append(gr.ChatMessage(role="assistant", content=loop_msg))
        time.sleep(1)
        yield state['chatbot_messages']

    print(f"Task '{state['task']}' completed. Thanks for using Teachmode-OOTB.")

@app.post("/update_params")
async def update_params(params: TaskParams):
    try:
        current_task.update(params.dict())
        
        # Update Gradio state
        demo_state = {
            "model": params.model,
            "task": params.task,
            "selected_screen": params.selected_screen,
            "user_id": params.user_id,
            "trace_id": params.trace_id,
            "api_keys": params.api_keys,
            "chatbot_messages": []
        }

        # Process the task
        process_input(params.task, demo_state)
        
        return {
            "success": True,
            "message": "Task started successfully",
            "params": current_task
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_gradio_interface():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        state = gr.State({})
        gr.Markdown("# Teach Mode Beta")

        with gr.Accordion("Settings", open=True): 
            with gr.Row():
                with gr.Column():
                    model = gr.Dropdown(
                        label="Model",
                        choices=["teach-mode-beta"],
                        value="teach-mode-beta",
                        interactive=False,
                    )
                with gr.Column():
                    provider = gr.Dropdown(
                        label="API Provider",
                        choices=["openai"],
                        value="openai",
                        interactive=False,
                    )
                with gr.Column():
                    api_key = gr.Textbox(
                        label="API Key",
                        type="password",
                        value="",
                        placeholder="No API key needed in beta",
                        interactive=False,
                    )
                with gr.Column():
                    screen_selector = gr.Dropdown(
                        label="Select Screen",
                        choices=SCREEN_NAMES,
                        value=SELECTED_SCREEN_INDEX,
                        interactive=False,
                    )

        with gr.Row():
            with gr.Column(scale=8):
                chat_input = gr.Textbox(
                    value=current_task["task"], 
                    show_label=False, 
                    container=False
                )
            with gr.Column(scale=1, min_width=50):
                submit_button = gr.Button(value="Send", variant="primary")

        chatbot = gr.Chatbot(
            label="Chatbot History", 
            autoscroll=True, 
            height=580, 
            type="messages"
        )

        def update_selected_screen(selected_screen_name, state):
            global SELECTED_SCREEN_INDEX
            SELECTED_SCREEN_INDEX = SCREEN_NAMES.index(selected_screen_name)
            state['selected_screen'] = SELECTED_SCREEN_INDEX

        screen_selector.change(
            fn=update_selected_screen, 
            inputs=[screen_selector, state], 
            outputs=None
        )
        submit_button.click(
            fn=process_input, 
            inputs=[chat_input, state], 
            outputs=chatbot
        )

        return demo

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run Teachmode-OOTB with FastAPI and Gradio interface"
    )
    parser.add_argument("--port", type=int, default=7888)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--model", default="teach-mode-gpt-4o")
    parser.add_argument("--task", default="")
    parser.add_argument("--selected_screen", type=int, default=0)
    parser.add_argument("--user_id", default="default_user")
    parser.add_argument("--trace_id", default="default_trace")
    parser.add_argument("--api_keys", default=None)
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Create Gradio interface
    demo = create_gradio_interface()
    
    # Mount Gradio app to FastAPI
    app.mount("/gradio", demo.app)
    
    # Run FastAPI server
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()