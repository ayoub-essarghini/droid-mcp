from .device_info import GetDeviceInfoTool
from .read_screen import ReadScreenTool
from .device_actions import TapScreenTool, PressButtonTool

android_tools = [
    GetDeviceInfoTool(),
    ReadScreenTool(),
    TapScreenTool(),
    PressButtonTool()
]