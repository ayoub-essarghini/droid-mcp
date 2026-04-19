from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class DeviceStatus(str, Enum):
    """
    Enumeration for Android device connection states.
    Helps the Agent understand if it can proceed with commands.
    """

    ONLINE = "online"
    OFFLINE = "offline"
    UNAUTHORIZED = "unauthorized"


class ActionResult(BaseModel):
    """
    Standard response format for any action executed on the Android device.
    Encapsulates success status, messages, and any returned data.
    """

    success: bool = Field(..., description="Indicates if the action was executed successfully")
    message: str = Field(..., description="Human-readable description of the result or error")
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Structured data returned by the tool (e.g., UI tree, battery info)",
    )


class ActionRequest(BaseModel):
    """
    Represents a request from the AI Agent to perform a specific task.
    """

    action_name: str = Field(..., description="The name of the tool to be invoked")
    params: Dict[str, Any] = Field(
        default_factory=dict, description="Key-value pairs required by the specific tool"
    )
