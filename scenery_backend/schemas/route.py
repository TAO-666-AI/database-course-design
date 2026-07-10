from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class RouteForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    difficulty: str = "easy"
    duration_hours: Decimal = Field(1, ge=0)
    spot_ids: list[int] = Field(default_factory=list)
