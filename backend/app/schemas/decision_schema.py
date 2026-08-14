from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DecisionRequest(BaseModel):
    recommendation_id: int
    action_taken: str
    override_reason: Optional[str] = None

class DecisionOut(BaseModel):
    id: int
    recommendation_id: int
    shipment_id: int
    action_taken: str
    override_reason: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True
