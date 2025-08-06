from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class Session(BaseModel):
    session_id: int = Field(min_value=1, default=1)
    session_user: str = Field(min_length=3, max_length=20)
    created_at: str = Field(default=datetime.now(timezone.utc).isoformat())

    model_config = {
        "json_schema_extra": {
            "example": {
                "session_user": "abc",
            }
        }
    }


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

    def __str__(self):
        return self.value


class Message(BaseModel):
    role: Role = Field(default=Role.USER)
    content: str = Field(min_length=3)

    model_config = {
        "json_schema_extra": {"example": {"role": Role.USER, "content": "Hello"}}
    }


class ChatHistory(BaseModel):
    session_id: int
    messages: list[Message]

    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": 1,
                "messages": [{"role": Role.USER, "content": "Hello"}],
            }
        }
    }
