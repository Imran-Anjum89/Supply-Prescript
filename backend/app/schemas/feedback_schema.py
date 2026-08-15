from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeedbackRequest(BaseModel):
    decision_id: int
    actual_delay_days: float
    actual_extra_cost: float = 0.0
    outcome_rating: int = 5
    notes: Optional[str] = ""

class FeedbackOut(BaseModel):
    id: int
    decision_id: int
    actual_delay_days: float
    actual_extra_cost: float
    outcome_rating: int
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
