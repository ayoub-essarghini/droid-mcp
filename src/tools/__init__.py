from .device_actions import (
    ExecuteShellTool,
    GetCrashLogsTool,
    GetDeviceStateTool,
    LongPressScreenTool,
    ManageNetworkTool,
    OpenApplicationTool,
    OpenUrlTool,
    PressButtonTool,
    SwipeScreenTool,
    TapScreenTool,
    TypeTextTool,
    WaitTool,
)
from .device_info import GetDeviceInfoTool
from .read_screen import ReadScreenTool

android_tools = [
    GetDeviceInfoTool(),
    ReadScreenTool(),
    TapScreenTool(),
    PressButtonTool(),
    TypeTextTool(),
    SwipeScreenTool(),
    LongPressScreenTool(),
    OpenApplicationTool(),
    OpenUrlTool(),
    ExecuteShellTool(),
    WaitTool(),
    ManageNetworkTool(),
    GetDeviceStateTool(),
    GetCrashLogsTool(),
]
