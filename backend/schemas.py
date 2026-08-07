from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ShipmentBase(BaseModel):
    shipment_id: str
    supplier: str
    destination: str
    status: str = "Pending"


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentResponse(ShipmentBase):
    id: int
    delay_probability: float
    risk_level: str
    created_at: datetime

    class Config:
        from_attributes = True


class SupplierBase(BaseModel):
    name: str
    location: Optional[str] = None
    reliability_score: float = 0.0


class SupplierCreate(SupplierBase):
    pass


class SupplierResponse(SupplierBase):
    id: int

    class Config:
        from_attributes = True


class PredictionResponse(BaseModel):
    shipment_id: str
    delay_probability: float
    predicted_delay_days: int
    risk_level: str

    class Config:
        from_attributes = True


class DecisionResponse(BaseModel):
    shipment_id: str
    recommendation: str
    accepted: bool

    class Config:
        from_attributes = True


class FeedbackCreate(BaseModel):
    shipment_id: str
    actual_delay_days: int
    comments: Optional[str] = None


class FeedbackResponse(FeedbackCreate):
    id: int

    class Config:
        from_attributes = True
      
