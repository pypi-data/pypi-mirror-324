import subprocess
import json
import os


def get_screenshot_external_cmd(selected_screen=0, python_exec="python"):
    """
    Spawns a new Python process that runs 'screenshot_cli.py' in a new CMD window
    (or at least a new process). Captures JSON from stdout and returns it.
    NOTE: 
    - This function is ***unreliable*** unless make sure nothing is printed to stdout in GUICapture.capture()
    - current_dir is set to the directory of the script
    """
    # 1) Build the command. Pass selected_screen as an argument
    cmd = [python_exec, "./computer_use_demo/gui_agent/gui_parser/uia_tools/screenshot_cli.py", str(selected_screen)]
    
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = os.getcwd()
    print(f"current_dir: {current_dir}")
    
    # 2) Run the command. 
    #    - capture_output=True: we get stdout/stderr in the result
    #    - text=True: decode the output as text automatically
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=current_dir)
    
    # 3) Check for errors
    if result.returncode != 0:
        # If the script failed, raise an exception with whatever is in stderr
        raise RuntimeError(f"Screenshot process failed:\n{result.stderr}")
    # print(f"subprocess result.stdout: {result.stdout}")

    # 4) Parse JSON from stdout
    stdout_str = result.stdout.strip()  # the JSON output
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



