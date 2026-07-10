from typing import Optional

from pydantic import BaseModel, Field


class ChatForm(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = Field(None, max_length=64)
