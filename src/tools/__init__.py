from .device_info import GetDeviceInfoTool

# Architect Note: We expose a list of tool instances here 
# so the Server can iterate through them and register them automatically.
android_tools = [
    GetDeviceInfoTool()
]