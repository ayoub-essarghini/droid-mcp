from typing import Optional

from ppadb.client import Client as AdbClient

from src.core.models import DeviceStatus


class ADBManager:
    """
    Manages the connection and communication with the Android device via ADB.
    Acts as a wrapper around the ppadb library to provide a clean interface.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 5037):
        self.host = host
        self.port = port
        self.client: Optional[AdbClient] = None
        self.device = None

    def connect(self) -> bool:
        """
        Initializes the ADB client and attempts to connect to the first available device.
        """
        try:
            self.client = AdbClient(host=self.host, port=self.port)
            devices = self.client.devices()

            if not devices:
                return False

            self.device = devices[0]
            return True
        except Exception:
            return False

    def check_status(self) -> DeviceStatus:
        """
        Verifies the current connection status of the device.
        """
        if not self.client:
            return DeviceStatus.OFFLINE

        try:
            devices = self.client.devices()
            if not devices:
                return DeviceStatus.OFFLINE
            return DeviceStatus.ONLINE
        except Exception:
            return DeviceStatus.OFFLINE

    async def execute_shell(self, command: str) -> str:
        """
        Executes a shell command on the device and returns the output.
        """
        if not self.device:
            raise ConnectionError("No Android device connected.")

        # Using the ppadb device shell execution
        return self.device.shell(command)

    def dump_ui_xml(self) -> str:
        """
        Captures the current UI hierarchy as an XML string.
        Essential for the 'Eyes' of the AI Agent.
        """
        if not self.device:
            raise ConnectionError("No Android device connected.")

        return self.device.shell("uiautomator dump /dev/tty")
