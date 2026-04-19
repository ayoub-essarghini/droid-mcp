from typing import Any, Dict

from src.core.base_tool import BaseAndroidTool
from src.core.models import ActionResult
from src.infrastructure import adb_manager
from src.infrastructure.ui_parser import AndroidUIParser


class ReadScreenTool(BaseAndroidTool):
    """
    Captures the current Android screen and returns a structured, parsed list of UI elements.
    This gives the AI "eyes" to see what is currently on the device.
    """

    @property
    def name(self) -> str:
        return "read_current_screen"

    @property
    def description(self) -> str:
        return (
            "Dumps the current Android UI hierarchy and returns "
            "a clean list of interactive elements. "
            "Use this tool to see what is on the screen before deciding where to click or type. "
            "Each element has a unique 'id' and 'bounds' (coordinates)."
        )

    @property
    def arguments_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {}, "required": []}

    async def run(self, **kwargs) -> ActionResult:
        try:
            if not adb_manager.device:
                if not adb_manager.connect():
                    return ActionResult(success=False, message="Device not connected.")

            #  Dump UI to a temporary file on the device
            # This is more stable than dumping directly to stdout
            await adb_manager.execute_shell("uiautomator dump /sdcard/window_dump.xml")

            # 2Read the dumped file
            raw_xml = await adb_manager.execute_shell("cat /sdcard/window_dump.xml")

            #  Parse and clean the XML
            parsed_ui = AndroidUIParser.parse_xml_to_json(raw_xml)

            if not parsed_ui:
                return ActionResult(
                    success=False, message="Failed to parse UI. Screen might be locked or empty."
                )

            return ActionResult(
                success=True,
                message=(
                    f"Successfully extracted {len(parsed_ui)} "
                    "interactive elements from the screen."
                ),
                data={"ui_elements": parsed_ui}
            )

        except Exception as e:
            return ActionResult(success=False, message=f"Error reading screen: {str(e)}")
