from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import ActionResult

class BaseAndroidTool(ABC):
    """
    Abstract Base Class (ABC) that defines the interface for all Android tools.
    Implements the Strategy Pattern to ensure consistent tool execution.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The unique identifier for the tool used by the MCP server.
        Example: 'android_click_element'
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Detailed description of the tool's functionality.
        The LLM uses this to decide when to call the tool.
        """
        pass

    @property
    @abstractmethod
    def arguments_schema(self) -> Dict[str, Any]:
        """
        Returns a JSON Schema (dict) defining the expected input parameters.
        Used for tool definition in the MCP protocol.
        """
        pass

    @abstractmethod
    async def run(self, **kwargs) -> ActionResult:
        """
        The core execution logic of the tool.
        Must be implemented by concrete classes to interact with the device.
        """
        pass