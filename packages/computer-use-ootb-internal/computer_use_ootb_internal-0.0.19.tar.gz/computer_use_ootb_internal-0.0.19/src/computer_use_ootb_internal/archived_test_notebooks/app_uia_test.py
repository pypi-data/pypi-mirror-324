import gradio as gr
from computer_use_ootb_internal.computer_use_demo.gui_agent.gui_parser.simple_parser.gui_capture import get_screenshot
from screenshot_service import ScreenshotService

def test_uia(state):


    input = state["input"]

    print(f"input: {input}")
    
    ss_service = state["screenshot_service"]

    uia_meta, sc_path = ss_service.get_screenshot()

    print(f"uia_meta: {uia_meta}, sc_path: {sc_path}")

    return "Hello " + f"uia_meta: {uia_meta}, sc_path: {sc_path}"


ss_service = ScreenshotService(selected_screen=0)

with gr.Blocks() as demo:
    state = gr.State({"screenshot_service": ss_service, "input": "test"})
    gr.Interface(fn=test_uia, inputs=state, outputs=gr.State())
demo.launch()