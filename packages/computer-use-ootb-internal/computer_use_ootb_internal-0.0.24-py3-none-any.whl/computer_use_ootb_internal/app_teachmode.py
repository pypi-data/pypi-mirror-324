import argparse
import time
import gradio as gr
import json
from fastapi import FastAPI, Request
import threading
from screeninfo import get_monitors
from computer_use_ootb_internal.computer_use_demo.tools.computer import get_screen_details
from computer_use_ootb_internal.run_teachmode_ootb_args import simple_teachmode_sampling_loop

app = FastAPI()

class SharedState:
    def __init__(self, args):
        self.args = args
        self.chatbot = None
        self.chat_input = None
        self.task_updated = False

shared_state = None

async def update_parameters(request: Request):
    global shared_state
    data = await request.json()
    shared_state.args = argparse.Namespace(**data)
    shared_state.task_updated = True
    return {"status": "success", "message": "Parameters updated", "new_args": vars(shared_state.args)}

def setup_state(state, args):
    state["model"] = args.model
    state["task"] = args.task
    state["selected_screen"] = args.selected_screen
    state["user_id"] = args.user_id
    state["trace_id"] = args.trace_id
    state["api_keys"] = args.api_keys
    state["server_url"] = args.server_url

    if 'chatbot_messages' not in state:
        state['chatbot_messages'] = []

def process_input(user_input, state):
    state['chatbot_messages'].append(gr.ChatMessage(role="user", content=user_input))
    yield state['chatbot_messages']

    print(f"start sampling loop: {state['chatbot_messages']}")

    sampling_loop = simple_teachmode_sampling_loop(
        model=state["model"],
        task=state["task"],
        selected_screen=state["selected_screen"],
        user_id=state["user_id"],
        trace_id=state["trace_id"],
        api_keys=state["api_keys"],
        server_url=state["server_url"],
    )

    for loop_msg in sampling_loop:
        print(f"loop_msg: {loop_msg}")
        state['chatbot_messages'].append(gr.ChatMessage(role="assistant", content=loop_msg))
        time.sleep(1)
        yield state['chatbot_messages']

    print(f"Task '{state['task']}' completed. Thanks for using Teachmode-OOTB.")

def update_input():
    while True:
        time.sleep(1)  # Check every second
        if shared_state and shared_state.task_updated:
            if shared_state.chat_input is not None:
                shared_state.chat_input.update(value=shared_state.args.task)
                shared_state.task_updated = False

def main():
    global app  # Add this line to use the global app variable
    
    parser = argparse.ArgumentParser(
        description="Run a synchronous sampling loop for assistant/tool interactions in teach-mode."
    )
    parser.add_argument("--model", default="teach-mode-gpt-4o")
    parser.add_argument("--task", default="Help me to complete the extraction of the viewer data of DeepSeek's first video on youtube, fill in the video name and the viewer data to excel sheet.")
    parser.add_argument("--selected_screen", type=int, default=0)
    parser.add_argument("--user_id", default="liziqi")
    parser.add_argument("--trace_id", default="default_trace")
    parser.add_argument("--api_key_file", default="api_key.json")
    parser.add_argument("--api_keys", default="")
    parser.add_argument(
        "--server_url",
        default="http://ec2-35-81-81-242.us-west-2.compute.amazonaws.com/generate_action",
        help="Server URL for the session (local='http://localhost:5000/generate_action', \
              aws='http://ec2-35-81-81-242.us-west-2.compute.amazonaws.com/generate_action').",
    )

    args = parser.parse_args()
    
    global shared_state
    shared_state = SharedState(args)

    # Start the polling thread
    polling_thread = threading.Thread(target=update_input, daemon=True)
    polling_thread.start()

    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        state = gr.State({})
        setup_state(state.value, args)
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
                        value=state.value.get("api_key", ""),
                        placeholder="No API key needed in beta",
                        interactive=False,
                    )
                with gr.Column():
                    screen_options, primary_index = get_screen_details()
                    screen_selector = gr.Dropdown(
                        label="Select Screen",
                        choices=screen_options,
                        value=args.selected_screen,
                        interactive=False,
                    )

        with gr.Row():
            with gr.Column(scale=8):
                chat_input = gr.Textbox(
                    value=args.task,
                    show_label=False,
                    container=False,
                    elem_id="chat_input"
                )
                shared_state.chat_input = chat_input
                
            with gr.Column(scale=1, min_width=50):
                submit_button = gr.Button(value="Send", variant="primary")

        chatbot = gr.Chatbot(
            label="Chatbot History",
            autoscroll=True,
            height=580,
            type="messages",
            elem_id="chatbot"
        )
        shared_state.chatbot = chatbot
        
        submit_button.click(fn=process_input, inputs=[chat_input, state], outputs=chatbot)

    # Add FastAPI endpoint before mounting Gradio
    app.add_route("/update_params", update_parameters, methods=["POST"])
    
    # Mount Gradio app to FastAPI
    app = gr.mount_gradio_app(app, demo, path="/")
    
    # Launch with uvicorn
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7888)

if __name__ == "__main__":
    main()