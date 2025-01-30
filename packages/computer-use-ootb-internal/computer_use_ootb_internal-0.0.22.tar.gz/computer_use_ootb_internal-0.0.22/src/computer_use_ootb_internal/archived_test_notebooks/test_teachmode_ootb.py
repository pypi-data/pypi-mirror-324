import os
import sys
import io
import logging
import time
import json
import platform
from typing import Callable
from enum import StrEnum
from collections.abc import Callable

import torch
from computer_use_ootb_internal.computer_use_demo.gui_agent.anthropic_agent import AnthropicActor
from computer_use_ootb_internal.computer_use_demo.executor.anthropic_executor import AnthropicExecutor
from computer_use_ootb_internal.computer_use_demo.executor.teachmode_executor import TeachModeExecutor
from computer_use_ootb_internal.computer_use_demo.gui_agent.actor.llm_actor import LLMActor
from computer_use_ootb_internal.computer_use_demo.gui_agent.planner.teach_mode_vlm_planner import TeachModeVLMPlanner, split_button_reference
from computer_use_ootb_internal.computer_use_demo.tools.screen_capture import get_screenshot
from computer_use_ootb_internal.computer_use_demo.gui_agent.gui_parser.simple_parser.gui_parser import parse_gui
from computer_use_ootb_internal.computer_use_demo.tools.colorful_text import colorful_text_vlm
from computer_use_ootb_internal.computer_use_demo.gui_agent.llm_utils.oai import encode_image

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define constants
BETA_FLAG = "computer-use-2024-10-22"


class APIProvider(StrEnum):
    ANTHROPIC = "anthropic"
    BEDROCK = "bedrock"
    VERTEX = "vertex"
    OPENAI = "openai"
    QWEN = "qwen"


PROVIDER_TO_DEFAULT_MODEL_NAME = {
    APIProvider.ANTHROPIC: "claude-3-5-sonnet-20241022",
    APIProvider.BEDROCK: "anthropic.claude-3-5-sonnet-20241022-v2:0",
    APIProvider.VERTEX: "claude-3-5-sonnet-v2@20241022",
}


def sampling_loop_sync(
    model: str,
    provider: APIProvider | None,
    system_prompt_suffix: str,
    messages: list[dict],
    output_callback: Callable[[str, str], None],
    tool_output_callback: Callable[[str, str], None],
    api_response_callback: Callable[[dict], None],
    api_key: str,
    only_n_most_recent_images: int | None = None,
    max_tokens: int = 4096,
    selected_screen: int = 0,
    user_id: str = None,
    trace_id: str = None
):
    """
    Synchronous sampling loop for assistant/tool interactions.
    """
    # Set device for model
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    print(f"Model initialized on device: {device}.")

    if model == "claude-3-5-sonnet-20241022":
        actor = AnthropicActor(
            model=model,
            provider=provider,
            system_prompt_suffix=system_prompt_suffix,
            api_key=api_key,
            api_response_callback=api_response_callback,
            max_tokens=max_tokens,
            only_n_most_recent_images=only_n_most_recent_images,
            selected_screen=selected_screen
        )
        executor = AnthropicExecutor(
            output_callback=output_callback,
            tool_output_callback=tool_output_callback,
            selected_screen=selected_screen
        )
    elif model.startswith("teach-mode"):
        executor = TeachModeExecutor(
            output_callback=output_callback,
            tool_output_callback=tool_output_callback,
            selected_screen=0
        )
        llm_mode = model.replace("teach-mode-", "")
        actor = LLMActor(llm_model=llm_mode, output_callback=output_callback, device=device, selected_screen=selected_screen)
        planner = TeachModeVLMPlanner(
            model=llm_mode,
            output_callback=output_callback,
            api_response_callback=api_response_callback,
            user_id=user_id,
            trace_id=trace_id,
            max_tokens=max_tokens,
            only_n_most_recent_images=only_n_most_recent_images,
            selected_screen=selected_screen,
            device=device,
            system_prompt_suffix=system_prompt_suffix
        )

        while True:
            print("Checking platform...")
            if platform.system() != "Windows":
                print("Teach mode supports only Windows.")
                # break
                # pass

            vlm_response = planner(messages=messages)
            next_action = json.loads(vlm_response).get("Next Action")
            next_action = split_button_reference(next_action)

            if not next_action:
                final_sc, final_sc_path = get_screenshot(selected_screen=selected_screen)
                output_callback(
                    f"No more actions. Task complete. Final State:\n<img src='data:image/png;base64,{encode_image(str(final_sc_path))}'>",
                    sender="bot"
                )
                break

            output_callback(f"Executing action: {next_action}", sender="bot")
            uia_data, screenshot_path = get_screenshot(selected_screen=selected_screen)
            gui = parse_gui(
                user_id=user_id,
                trace_id=trace_id,
                screenshot_path=screenshot_path,
                query=next_action,
                mode="teach"
            )
            actor_response = actor(next_action, gui, screenshot_path)
            messages.append({"role": "user", "content": actor_response["content"]})

            for message in executor(actor_response, messages):
                yield message

    else:
        raise ValueError("Invalid model selected.")


# Callbacks
def output_callback(response, sender):
    print(f"[{sender}]: {response}")


def api_response_callback(response, sender):
    print(f"[API]: {response}")


def tool_output_callback(tool_result, sender):
    print(f"[Tool]: {tool_result}")


# Environment setup
os.environ["OPENAI_API_KEY"] = "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"
os.environ["GEMINI_API_KEY"] = "AIzaSyDgjkdmiKIzbDk3QjXoviLMQDMtpYps7gM"
os.environ["OOTB_PATH"] = r"./computer_use_demo"
os.environ['GOOGLE_API_KEY'] = "AIzaSyA5v66c7lIhpAjpxiflKY4VU41AGHcENHM"

# Example usage
messages = [{"role": "user",
             "content": "Help me to complete the mission 'Buds of Memories' in Star Rail"}]

sampling_loop = sampling_loop_sync(
    model="teach-mode-gpt-4o-mini",
    provider=None,
    system_prompt_suffix="",
    messages=messages,
    output_callback=output_callback,
    tool_output_callback=tool_output_callback,
    api_response_callback=api_response_callback,
    api_key="your-api-key",
    selected_screen=0,
    user_id="star_rail",
    trace_id="default_trace"
)

for step in sampling_loop:
    print(step)
    time.sleep(2)