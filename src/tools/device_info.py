import re
from typing import Dict, Any
from src.core.base_tool import BaseAndroidTool
from src.core.models import ActionResult
from src.infrastructure import adb_manager

class GetDeviceInfoTool(BaseAndroidTool):
    """
    Tool to retrieve hardware and software information from the Android device.
    Useful for the Agent to know the environment it's working in.
    """

    @property
    def name(self) -> str:
        return "get_android_device_info"

    @property
    def description(self) -> str:
        return (
            "Returns technical details about the connected Android device, "
            "including battery level, screen resolution, and OS version."
        )

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        # This tool doesn't need any input parameters from the LLM
        return {
            "type": "object",
            "properties": {},
            "required": []
        }

    async def run(self, **kwargs) -> ActionResult:
        try:
            #  Ensure device is connected
            if not adb_manager.device:
                connected = adb_manager.connect()
                if not connected:
                    return ActionResult(success=False, message="No Android device detected via ADB.")

            # Execute ADB commands to gather data
            battery_raw = await adb_manager.execute_shell("dumpsys battery")
            version = await adb_manager.execute_shell("getprop ro.build.version.release")
            model = await adb_manager.execute_shell("getprop ro.product.model")
            wm_size = await adb_manager.execute_shell("wm size")

            #  Simple regex parsing for battery level
            battery_level = "Unknown"
            level_match = re.search(r"level: (\d+)", battery_raw)
            if level_match:
                battery_level = f"{level_match.group(1)}%"

            #  Construct the success result
            device_data = {
                "model": model.strip(),
                "android_version": version.strip(),
                "battery": battery_level,
                "screen_resolution": wm_size.strip().replace("Physical size: ", "")
            }

            return ActionResult(
                success=True,
                message="Device information retrieved successfully.",
                data=device_data
            )

        except Exception as e:
            return ActionResult(
                success=False, 
                message=f"Error retrieving device info: {str(e)}"
            )