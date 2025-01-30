import json
import uiautomation as auto
import time
import subprocess
import pygetwindow as gw
from pywinauto import Application, Desktop
import os
import re
import datetime
import requests
import time
from termcolor import colored
import subprocess
import win32gui
import win32process
import psutil
from PIL import Image, ImageDraw
import base64
import pickle
import requests
from PIL import Image, ImageDraw
# from pywinauto.application import Application
from pywinauto.findwindows import find_windows


software_name_map = {"adobe_acrobat": "Adobe Acrobat", "premiere_pro": "Adobe Premiere Pro"}
    
def get_screenshot(software_name=None):
    software_name = software_name_map.get(software_name, software_name)
    gui = GUICapture()
    meta_data, screenshot_path = gui.capture(software=software_name)
    return meta_data, screenshot_path


def get_control_properties(control, properties_list, no_texts=False):
    prop_dict = {}
    for prop in properties_list:
        # Skip 'texts' property if no_texts flag is set
        if no_texts and prop in ['texts', "friendly_class_name", "automation_id", "rectangle", "UIA_ImageControlTypeId"]:
            prop_dict[prop] = ['']  # Use an empty list as a placeholder
            continue

        # Check if the control has the property as an attribute
        if hasattr(control, prop):
            attr = getattr(control, prop)
            # Ensure the attribute is callable before attempting to call it
            if callable(attr):
                try:
                    value = attr()
                    # Special handling for 'rectangle' property
                    if prop == 'rectangle':
                        value = [value.left, value.top, value.right, value.bottom]
                    prop_dict[prop] = value
                except Exception:
                    # If there's an exception, such as a method failing, we skip it
                    continue
            else:
                # If the attribute is not callable, directly assign it
                prop_dict[prop] = attr
    return prop_dict


class GUICapture:
    """
    A class to capture and interact with a GUI of a specified application.
    """
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    END = '\033[0m'

    def __init__(self, cache_folder='.cache/'):
        """
        Initialize the GUICapture instance.
        """
        self.task_id = self.get_current_time()
        self.cache_folder = os.path.join(cache_folder, self.task_id)
        os.makedirs(self.cache_folder, exist_ok=True)
        self.current_step = 0
        self.history = []
        self.port = 6007      

    def capture(self, software=None):
        """
        Execute the capture process.
        """
        start = time.time()
        # time.sleep(2)  # Consider explaining why this delay is necessary

        if software is None:
            software = self.get_topest_window()

        self.connect_to_application(software)
        meta_data = self.get_gui_meta_data(software)
        screenshot_path = self.capture_screenshot()
        print(f"Time used: {time.time() - start}")
        start = time.time()
        return meta_data, screenshot_path
    
    def get_topest_window(self):
        # Find the window of interest (replace 'Window Title' with the actual title)
        all_window_titles = gw.getAllTitles()

        for window_title in all_window_titles:
            # if 'Window Title' in window:
            win = gw.getWindowsWithTitle(window_title)[0]
            if window_title != "":
                print(f"Top position of the window '{window_title}': {win.top}")
                break

        return window_title
    
    def connect_to_application(self, software_name):
        """
        Connect to the target application.
        """
        try:
            window_handles = find_windows(title_re=f".*{software_name}*", visible_only=False)
            # print(window_handles)
            self.app = Application(backend="uia").connect(handle=window_handles[0])
            # self.app = Application(backend="uia").connect(title_re=f".*{software_name}*")
        except Exception as e:
            print(f"Error connecting to application: {e}")
            try:
                print("Try to connect to the application by using the window name.")
                self.app = self.detect_duplicate_name_windows(software_name)
            except Exception as e:
                print(f"Error connecting to application: {e}")

    def detect_duplicate_name_windows(self, software_name):
        # 使用find_windows函数查找所有匹配的窗口句柄
        window_handles = find_windows(title_re=f".*{software_name}*", visible_only=False)

        # 检查找到的窗口句柄数量
        if window_handles:
            # 假设我们想要连接到找到的第一个窗口
            first_window_handle = window_handles[0]

            # 使用窗口句柄连接到应用程序
            app = Application(backend="uia").connect(handle=first_window_handle)
            # app = Application(backend="uia").connect(handle=first_window_handle)

            return app
            # # 通过app对象操作窗口
            # # 例如，获取窗口的主窗口对象并进行操作
            # main_window = app.window(handle=first_window_handle)
            # # 现在可以对main_window进行操作，例如点击按钮、输入文本等

        else:
            print("没有找到匹配的窗口")
            return None

    def get_gui_meta_data(self, software):
        # Connect to the application
        # Initialize data storage
        control_properties_list = ['friendly_class_name', 'texts', 'rectangle', 'automation_id']
        th = 1000 # software_th.get(software, 100)

        def recurse_controls(control, current_depth=0):

            # from IPython.core.debugger import Pdb; Pdb().set_trace()

            children = control.children()

            child_data = []
            if current_depth > th:
                return []
        
            for child in children:
                # check if the control is visible
                if not child.is_visible():
                    continue  

                properties = get_control_properties(child, control_properties_list)

                # Check if the control is a ComboBox, which may encounter bug while acquire text
                no_texts = True if properties.get('friendly_class_name') == 'ComboBox' else False
                # no_texts = False
                    
                child_data.append({
                    'properties': get_control_properties(child, control_properties_list, no_texts=no_texts),
                    'children': recurse_controls(child, current_depth + 1)
                })

            return child_data

        all_windows = self.app.windows()
        window_names = [window.window_text() for window in all_windows]
        meta_data = {}
        for window_name in window_names:
            # from IPython.core.debugger import Pdb; Pdb().set_trace()

            if window_name:
                print(window_name)
                target_window = self.app.window(title=window_name)
                print(target_window)
                # target_window.set_focus()

                # Traverse the control tree
                meta_data[window_name] = recurse_controls(target_window)

        return meta_data

    def capture_screenshot(self, save_path=None):
        # save screenshot and return path
        if save_path:
            screenshot_path = save_path
        else:
            screenshot_path = os.path.join(self.cache_folder, f'screenshot-{self.current_step}.png')

        screenshot = auto.GetRootControl().ToBitmap()
        screenshot.ToFile(screenshot_path)
        return screenshot_path

    @staticmethod
    def get_current_time():
        return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


def get_all_windows():
    all_windows = gw.getAllWindows()
    all_windows_name = [win.title for win in all_windows if win.title]
    all_windows_name = simplify_window_names(all_windows_name)
    return all_windows_name


def simplify_window_names(names):
    simplified_names = []
    for name in names:
        # Split the name by '-' and strip whitespace
        parts = [part.strip() for part in name.split('-')]
        # Use the part after the last '-' if available, otherwise the original name
        simplified_name = parts[-1] if len(parts) > 1 else name
        simplified_names.append(simplified_name)
    return simplified_names


def maximize_window(title):
    """Maximize the window"""
    windows = gw.getWindowsWithTitle(title)
    if windows:
        window = windows[0]  # Assume the first window is target window
        if not window.isMaximized:
            window.maximize()
            print(f"Window '{title}' has been maximized.")
        else:
            print(f"Window '{title}' is already maximized.")
    else:
        print(f"No window with the title '{title}' found.")


def extract_texts_and_rectangles(data):
    result = []
    
    def traverse(node):
        # Extract the current node's text and rectangle
        if 'properties' in node:
            texts = node['properties'].get('texts', [])
            rectangle = node['properties'].get('rectangle', [])
            if texts and len(texts) > 0 and rectangle:
                result.append([texts[0], rectangle])
        
        # Traverse children if they exist
        if 'children' in node:
            for child in node['children']:
                traverse(child)
    
    traverse(data[0])  # Assuming the data is a list with one top-level item
    return result


def visualize(gui, screenshot_path, if_show=True):
    ui_elements = []

    def extract_elements(node):
        if isinstance(node, list):
            for item in node:
                extract_elements(item)
        elif isinstance(node, dict):
            properties = node.get('properties', {})
            texts = properties.get('texts', [])
            rectangle = properties.get('rectangle', [])
            if rectangle and texts:
                # Use the first text as the name or join all texts
                # name = texts[0] if texts else ''
                name = texts
                ui_elements.append((name, rectangle))
            # Recurse into children
            children = node.get('children', [])
            extract_elements(children)

    for window_name, panels in gui.items():
        extract_elements(panels)

    image = Image.open(screenshot_path)
    draw = ImageDraw.Draw(image)

    # Draw rectangles and text
    for element in ui_elements:
        name, rectangle = element
        try:
            # print(type(name))
            if isinstance(name, list) and len(name) == 1:
                name = name[0].encode('latin-1', 'ignore').decode('latin-1')
            else:
                name = name.encode('latin-1', 'ignore').decode('latin-1')
                # name = name[0].encode('latin-1', 'ignore').decode('latin-1')
        except:
            print(name)
            name = ""
        # Draw rectangle in red
        try:
            draw.rectangle(rectangle, outline="red")
            # Calculate text position above the rectangle
            text_position = (rectangle[0]-15, rectangle[1] - 15)  # Positioned above the rectangle
            draw.text(text_position, name, fill="red")  # Default font
        except:
            print(rectangle)
            print(name)


    # if if_show:
    #     display(image)
    return image


def encode_image(image_path):
    """Encode image file to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def encode_task(task):
    if isinstance(task, str):
        return task
    else:
        return base64.b64encode(pickle.dumps(task)).decode('utf-8')
    
def send_gui_parser_request(url, software_name, screenshot_path, meta_data, task_id=None, step_id=None):
    """Send a POST request to the server with the query and the image."""
    # Encode the image
    screenshot_data = encode_image(screenshot_path)
    
    # Construct the request data
    data = {
        "screenshot": screenshot_data,
        "GUI": meta_data,
        "software_name": software_name,
        "task_id": task_id,
        "step_id": step_id
    }
    
    # Send POST request
    response = requests.post(url, json=data)
    return response.json()


def send_actor_request(url, 
                       current_task, 
                       parsed_screenshot,
                       screenshot_path: str, 
                       software_name: str, 
                       history: list=[], 
                       error_message: str="", 
                       next_step_tip: str="", 
                       pre_act_success_flag: bool=False, 
                       pre_act_resume_flag: bool=False, 
                       task_id: str=None, 
                       step_id: str=None):
    """Send a POST request to the server with the query and the image."""
    # Encode the image
    screenshot_data = encode_image(screenshot_path)
        
    # Construct the request data
    data = {
        "current_task": encode_task(current_task),
        "parsed_screenshot": parsed_screenshot,
        "screenshot": screenshot_data,
        "history": history,
        "error_message": error_message,
        "next_step": next_step_tip,
        "pre_act_success_flag": pre_act_success_flag,
        "pre_act_resume_flag": pre_act_resume_flag,
        "software_name": software_name,
        "task_id": task_id,
        "step_id": step_id, 
    }
    
    # Send POST request
    response = requests.post(url, json=data)
    return response.json()

if __name__ == '__main__':
    capture = GUICapture('Adobe Premiere Pro')
    meta_data, screenshot_path = capture.run("None", send_data=False)
