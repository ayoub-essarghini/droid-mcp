from .device_info import GetDeviceInfoTool
from .read_screen import ReadScreenTool

# List of all available tools
android_tools = [
    GetDeviceInfoTool(),
    ReadScreenTool()
]