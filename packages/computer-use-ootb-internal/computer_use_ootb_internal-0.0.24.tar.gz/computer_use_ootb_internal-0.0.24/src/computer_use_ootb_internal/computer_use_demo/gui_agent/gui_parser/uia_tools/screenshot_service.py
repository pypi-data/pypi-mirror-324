import subprocess
import json
import os
from importlib import resources
from pathlib import Path

def get_screenshot_external_cmd(selected_screen=0, python_exec="python"):
    """
    Spawns a new Python process that runs 'screenshot_cli.py' in a new CMD window
    (or at least a new process). Captures JSON from stdout and returns it.
    NOTE: 
    - This function is ***unreliable*** unless make sure nothing is printed to stdout in GUICapture.capture()
    """
    # Get the path to screenshot_cli.py using importlib.resources
    try:
        with resources.path('computer_use_ootb_internal.computer_use_demo.gui_agent.gui_parser.uia_tools', 'screenshot_cli.py') as script_path:
            script_path = str(script_path)
    except Exception as e:
        print(f"Error finding resource path: {e}")
        raise

    # Build the command with the resolved path
    cmd = [python_exec, script_path, str(selected_screen)]
    
    # Get the package directory path
    try:
        with resources.path('computer_use_ootb_internal', '') as package_path:
            current_dir = str(package_path)
    except Exception as e:
        print(f"Error finding package path: {e}")
        raise

    print(f"current_dir: {current_dir}")
    print(f"script_path: {script_path}")
    
    # Run the command
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=current_dir)
    
    # Check for errors
    if result.returncode != 0:
        raise RuntimeError(f"Screenshot process failed:\n{result.stderr}")

    # Parse JSON from stdout
    stdout_str = result.stdout.strip()
    try:
        data = json.loads(stdout_str)
        meta_data = data["meta_data"]
        screenshot_path = data["screenshot_path"]
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned: {stdout_str}") from e
    
    return meta_data, screenshot_path

if __name__ == "__main__":
    meta_data, screenshot_path = get_screenshot_external_cmd(selected_screen=0)
    print(f"[get_screenshot_external_cmd] meta_data: {meta_data}, screenshot_path: {screenshot_path}")