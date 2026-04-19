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
