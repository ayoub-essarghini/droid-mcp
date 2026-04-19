from .device_actions import PressButtonTool, TapScreenTool
from .device_info import GetDeviceInfoTool
from .read_screen import ReadScreenTool

android_tools = [GetDeviceInfoTool(), ReadScreenTool(), TapScreenTool(), PressButtonTool()]
