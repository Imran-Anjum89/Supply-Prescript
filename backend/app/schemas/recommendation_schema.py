from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RecommendRequest(BaseModel):
    shipment_id: int
    max_budget_extra: float = 1200.0

class RecommendationOut(BaseModel):
    id: int
    shipment_id: int
    suggested_action: str
    expedited_carrier: Optional[str] = None
    estimated_extra_cost: float
    time_saved_days: float
    roi_score: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
