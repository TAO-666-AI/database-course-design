from typing import Optional

from pydantic import BaseModel, Field


class FeedbackForm(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)
    rating: int = Field(..., ge=1, le=5)
    content: str = Field(..., min_length=1, max_length=1000)


class FeedbackStatusForm(BaseModel):
    status: str
    reply: Optional[str] = Field(None, max_length=1000)
