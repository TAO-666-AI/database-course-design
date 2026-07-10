from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class SpotForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    open_time: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=100)
    ticket_price: Decimal = Field(0, ge=0)
    recommended_duration: Optional[str] = Field(None, max_length=50)
    image_url: Optional[str] = Field(None, max_length=255)
    status: str = "active"
