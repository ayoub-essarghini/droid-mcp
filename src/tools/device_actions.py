import asyncio
from typing import Any, Dict

from src.core.base_tool import BaseAndroidTool
from src.core.models import ActionResult
from src.infrastructure import adb_manager


class TapScreenTool(BaseAndroidTool):
    """
    Taps the Android screen at specific X, Y coordinates.
    The AI uses this after reading the screen bounds.
    """

    @property
    def name(self) -> str:
        return "tap_screen"

    @property
    def description(self) -> str:
        return (
            "Taps the device screen at the given (x, y) coordinates. "
            "To tap a UI element, calculate its center from its bounds [x1, y1, x2, y2] "
            "using: x = (x1 + x2) / 2 and y = (y1 + y2) / 2."
        )

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "The X coordinate to tap"},
                "y": {"type": "integer", "description": "The Y coordinate to tap"},
            },
            "required": ["x", "y"],
        }

    async def run(self, **kwargs) -> ActionResult:
        x = kwargs.get("x")
        y = kwargs.get("y")

        if x is None or y is None:
            return ActionResult(success=False, message="Missing x or y coordinates.")

        try:
            if not adb_manager.device:
                adb_manager.connect()

            # Execute the ADB input tap command
            await adb_manager.execute_shell(f"input tap {x} {y}")

            return ActionResult(success=True, message=f"Successfully tapped screen at ({x}, {y}).")
        except Exception as e:
            return ActionResult(success=False, message=f"Failed to tap: {str(e)}")


class PressButtonTool(BaseAndroidTool):
    """
    Simulates pressing hardware/system buttons (Home, Back, Enter).
    """

    @property
    def name(self) -> str:
        return "press_button"

    @property
    def description(self) -> str:
        return "Presses a system navigation button. Allowed values: 'home', 'back', 'enter'."

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "button": {
                    "type": "string",
                    "enum": ["home", "back", "enter"],
                    "description": "The button to press",
                }
            },
            "required": ["button"],
        }

    async def run(self, **kwargs) -> ActionResult:
        button = kwargs.get("button")

        # ADB keyevent mapping
        key_map = {
            "home": "3",  # KEYCODE_HOME
            "back": "4",  # KEYCODE_BACK
            "enter": "66",  # KEYCODE_ENTER
        }

        keycode = key_map.get(button)
        if not keycode:
            return ActionResult(success=False, message=f"Unsupported button: {button}")

        try:
            if not adb_manager.device:
                adb_manager.connect()

            await adb_manager.execute_shell(f"input keyevent {keycode}")
            return ActionResult(success=True, message=f"Pressed '{button}' button.")
        except Exception as e:
            return ActionResult(success=False, message=f"Failed to press button: {str(e)}")
class TypeTextTool(BaseAndroidTool):
    """
    Types text into the currently focused text field on the Android device.
    """

    @property
    def name(self) -> str:
        return "type_text"

    @property
    def description(self) -> str:
        return (
            "Types text into the currently focused text field. "
            "IMPORTANT: You must tap on a text box to focus it BEFORE using this tool."
        )

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to type"},
            },
            "required": ["text"],
        }

    async def run(self, **kwargs) -> ActionResult:
        text = kwargs.get("text")
        if not text:
            return ActionResult(success=False, message="Missing text argument.")

        try:
            if not adb_manager.device:
                adb_manager.connect()

            # ADB requires spaces to be replaced with %s
            formatted_text = str(text).replace(" ", "%s")

            # Using quotes to escape special characters in the shell
            await adb_manager.execute_shell(f"input text '{formatted_text}'")

            return ActionResult(success=True, message=f"Successfully typed: {text}")
        except Exception as e:
            return ActionResult(success=False, message=f"Failed to type text: {str(e)}")


class SwipeScreenTool(BaseAndroidTool):
    """
    Swipes on the screen from starting coordinates (x1, y1) to ending coordinates (x2, y2).
    """

    @property
    def name(self) -> str:
        return "swipe_screen"

    @property
    def description(self) -> str:
        return (
            "Swipes on the screen from (x1, y1) to (x2, y2). "
            "Useful for scrolling menus (swipe up/down) or swiping between pages."
        )

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "x1": {"type": "integer", "description": "Starting X coordinate"},
                "y1": {"type": "integer", "description": "Starting Y coordinate"},
                "x2": {"type": "integer", "description": "Ending X coordinate"},
                "y2": {"type": "integer", "description": "Ending Y coordinate"},
                "duration_ms": {
                    "type": "integer",
                    "description": "Duration of swipe in ms (e.g., 300 is fast, 1000 is slow)",
                },
            },
            "required": ["x1", "y1", "x2", "y2"],
        }

    async def run(self, **kwargs) -> ActionResult:
        x1 = kwargs.get("x1")
        y1 = kwargs.get("y1")
        x2 = kwargs.get("x2")
        y2 = kwargs.get("y2")
        duration_ms = kwargs.get("duration_ms", 500)

        if None in (x1, y1, x2, y2):
            return ActionResult(success=False, message="Missing coordinates for swipe.")

        try:
            if not adb_manager.device:
                adb_manager.connect()

            await adb_manager.execute_shell(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")

            return ActionResult(
                success=True,
                message=f"Successfully swiped from ({x1}, {y1}) to ({x2}, {y2})."
            )
        except Exception as e:
            return ActionResult(success=False, message=f"Failed to swipe: {str(e)}")
class LongPressScreenTool(BaseAndroidTool):
    """
    Long presses the Android screen at specific X, Y coordinates.
    Useful for opening context menus or selecting items.
    """

    @property
    def name(self) -> str:
        return "long_press_screen"

    @property
    def description(self) -> str:
        return (
            "Long presses the screen at the given (x, y) coordinates. "
            "This is used to bring up context menus or select text."
        )

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "The X coordinate"},
                "y": {"type": "integer", "description": "The Y coordinate"},
                "duration_ms": {
                    "type": "integer",
                    "description": "Duration in ms (default is 1000ms for a long press)",
                },
            },
            "required": ["x", "y"],
        }

    async def run(self, **kwargs) -> ActionResult:
        x = kwargs.get("x")
        y = kwargs.get("y")
        duration_ms = kwargs.get("duration_ms", 1000)

        if x is None or y is None:
            return ActionResult(success=False, message="Missing coordinates.")

        try:
            if not adb_manager.device:
                adb_manager.connect()

            # ADB "swipe" in the same place is the official way to do a long press
            await adb_manager.execute_shell(f"input swipe {x} {y} {x} {y} {duration_ms}")
            return ActionResult(success=True, message=f"Long pressed at ({x}, {y}).")
        except Exception as e:
            return ActionResult(success=False, message=f"Failed to long press: {str(e)}")


class OpenApplicationTool(BaseAndroidTool):
    """
    Opens an application directly using its Android package name.
    """

    @property
    def name(self) -> str:
        return "open_application"

    @property
    def description(self) -> str:
        return (
            "Opens an Android app directly using its package name. "
            "CRITICAL HUMAN BEHAVIOR RULE: BEFORE you use this tool, you MUST ALWAYS "
            "use 'get_device_state' first. If the app is already in the foreground, "
            "DO NOT use this tool. Just proceed with your task."
        )

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "package_name": {"type": "string", "description": "The Android package name"},
            },
            "required": ["package_name"],
        }

    async def run(self, **kwargs) -> ActionResult:
        package_name = kwargs.get("package_name")
        if not package_name:
            return ActionResult(success=False, message="Missing package name.")

        try:
            if not adb_manager.device:
                adb_manager.connect()

            # The monkey command is the most reliable way to launch an app's main activity
            await adb_manager.execute_shell(
                f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
            )
            return ActionResult(success=True, message=f"Launched application: {package_name}")
        except Exception as e:
            return ActionResult(success=False, message=f"Failed to launch app: {str(e)}")


class OpenUrlTool(BaseAndroidTool):
    """
    Opens a specific URL in the device's default web browser.
    """

    @property
    def name(self) -> str:
        return "open_url"

    @property
    def description(self) -> str:
        return "Opens a web URL directly in the Android default browser."

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The full URL to open (e.g., https://...)"},
            },
            "required": ["url"],
        }

    async def run(self, **kwargs) -> ActionResult:
        url = kwargs.get("url")
        if not url:
            return ActionResult(success=False, message="Missing URL.")

        try:
            if not adb_manager.device:
                adb_manager.connect()

            await adb_manager.execute_shell(f"am start -a android.intent.action.VIEW -d '{url}'")
            return ActionResult(success=True, message=f"Opened URL: {url}")
        except Exception as e:
            return ActionResult(success=False, message=f"Failed to open URL: {str(e)}")


class ExecuteShellTool(BaseAndroidTool):
    """
    The Ultimate Power Tool: Allows the AI to run raw ADB shell commands.
    """

    @property
    def name(self) -> str:
        return "execute_adb_shell"

    @property
    def description(self) -> str:
        return (
            "Executes a raw ADB shell command. Use this only if other tools are insufficient. "
            "Examples: 'input keyevent 24' (Volume Up), 'am force-stop com.whatsapp' (Close app)."
        )

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The raw shell command (without 'adb shell')"},
            },
            "required": ["command"],
        }

    async def run(self, **kwargs) -> ActionResult:
        command = kwargs.get("command")
        if not command:
            return ActionResult(success=False, message="Missing command.")

        try:
            if not adb_manager.device:
                adb_manager.connect()

            result = await adb_manager.execute_shell(command)
            return ActionResult(
                success=True,
                message=f"Executed: {command}\nOutput: {result.strip() if result else 'Success'}"
            )
        except Exception as e:
            return ActionResult(success=False, message=f"Shell command failed: {str(e)}")

class WaitTool(BaseAndroidTool):
    """
    Pauses execution for a specified number of seconds to allow UI elements to load.
    """

    @property
    def name(self) -> str:
        return "wait"

    @property
    def description(self) -> str:
        return (
            "Waits for a specified number of seconds. "
            "CRITICAL: Always use this tool after opening an app, clicking a link, "
            "or doing anything that requires the screen to load or animate, before taking the next action."
        )

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "seconds": {
                    "type": "integer",
                    "description": "Number of seconds to wait (e.g., 2, 3, 5)"
                },
            },
            "required": ["seconds"],
        }

    async def run(self, **kwargs) -> ActionResult:
        seconds = kwargs.get("seconds", 2)
        try:
            await asyncio.sleep(seconds)
            return ActionResult(success=True, message=f"Waited for {seconds} seconds. The UI should now be settled.")
        except Exception as e:
            return ActionResult(success=False, message=f"Wait interrupted: {str(e)}")

class ManageNetworkTool(BaseAndroidTool):
    """
    Manages the device's network connection (Check status, turn Wi-Fi on/off).
    """

    @property
    def name(self) -> str:
        return "manage_network"

    @property
    def description(self) -> str:
        return (
            "Checks or modifies the device's network connection. "
            "Actions: 'status' (ping test), 'wifi_on' (enable Wi-Fi), 'wifi_off' (disable Wi-Fi)."
        )

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["status", "wifi_on", "wifi_off"],
                    "description": "The network action to perform",
                },
            },
            "required": ["action"],
        }

    async def run(self, **kwargs) -> ActionResult:
        action = kwargs.get("action")

        if not action:
            return ActionResult(success=False, message="Missing network action.")

        try:
            if not adb_manager.device:
                adb_manager.connect()

            if action == "status":
                # Check internet by pinging Google DNS with 1 packet
                result = await adb_manager.execute_shell("ping -c 1 8.8.8.8")
                # ping command returns different formats, but "1 packets transmitted" or "ttl=" is a good sign
                if result and ("1 packets transmitted, 1 received" in result or "ttl=" in result.lower()):
                    return ActionResult(success=True, message="Internet is connected and working.")
                else:
                    return ActionResult(
                        success=False,
                        message="No active internet connection. Try turning on Wi-Fi."
                    )

            elif action == "wifi_on":
                await adb_manager.execute_shell("svc wifi enable")
                return ActionResult(success=True, message="Wi-Fi has been turned ON.")

            elif action == "wifi_off":
                await adb_manager.execute_shell("svc wifi disable")
                return ActionResult(success=True, message="Wi-Fi has been turned OFF.")

            else:
                return ActionResult(success=False, message=f"Unknown action: {action}")

        except Exception as e:
            return ActionResult(success=False, message=f"Network operation failed: {str(e)}")
class GetDeviceStateTool(BaseAndroidTool):
    """
    Checks the current exact state of the device (Screen ON/OFF, Locked/Unlocked, Foreground App).
    The AI should ALWAYS use this before deciding to open an app.
    """

    @property
    def name(self) -> str:
        return "get_device_state"

    @property
    def description(self) -> str:
        return (
            "Returns the current state of the device including: "
            "1. Is the screen ON or OFF? "
            "2. What is the current foreground application (package name)? "
            "CRITICAL: Always run this first to check if your target app is ALREADY open before launching it."
        )

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {}, 
        }

    async def run(self, **kwargs) -> ActionResult:
        try:
            if not adb_manager.device:
                adb_manager.connect()

            #  Check if screen is ON or OFF
            power_state = await adb_manager.execute_shell("dumpsys power | grep 'Display Power: state='")
            is_screen_on = "ON" in (power_state or "").upper()

            # Check the current foreground application
            focus = await adb_manager.execute_shell("dumpsys window | grep mCurrentFocus")
            
            # Extract package name (e.g., from "mCurrentFocus=Window{... u0 com.android.chrome/...}")
            current_app = "Unknown"
            if focus and "mCurrentFocus=Window" in focus:
                try:
                    # Parsing the package name from the dumpsys string
                    parts = focus.split(" ")
                    for part in parts:
                        if "/" in part and "{" not in part and "}" not in part:
                            current_app = part.split("/")[0]
                            break
                except Exception:
                    current_app = focus.strip()

            state_report = (
                f"Device State Report:\n"
                f"- Screen Status: {'ON' if is_screen_on else 'OFF'}\n"
                f"- Current Foreground App: {current_app}\n"
            )

            return ActionResult(success=True, message=state_report)
        except Exception as e:
            return ActionResult(success=False, message=f"Failed to get device state: {str(e)}")