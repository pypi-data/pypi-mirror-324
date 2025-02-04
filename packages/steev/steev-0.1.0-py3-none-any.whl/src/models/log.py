from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class LogLevel(str, Enum):
    INFO = "INFO"
    ERROR = "ERROR"


class LogModel(BaseModel):
    """Log model for both HTTP and WebSocket communication"""

    message: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    level: Literal["INFO", "ERROR"] = Field("INFO", description="Log level")
