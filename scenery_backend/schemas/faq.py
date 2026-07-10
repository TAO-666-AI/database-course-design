from typing import Optional

from pydantic import BaseModel, Field


class FAQForm(BaseModel):
    question: str = Field(..., min_length=1, max_length=255)
    answer: str = Field(..., min_length=1)
    category: Optional[str] = Field(None, max_length=50)
    keywords: Optional[str] = Field(None, max_length=255)
    sort_order: int = 0
