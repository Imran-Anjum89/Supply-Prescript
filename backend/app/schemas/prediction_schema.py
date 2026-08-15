from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class PredictRequest(BaseModel):
    shipment_id: int

class PredictionOut(BaseModel):
    id: int
    shipment_id: int
    delay_probability: float
    predicted_delay_days: float
    risk_level: str
    feature_contributions: Optional[Dict[str, Any]] = None
    model_version: str
    created_at: datetime

    class Config:
        from_attributes = True
