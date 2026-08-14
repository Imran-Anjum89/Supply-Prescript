from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShipmentCreate(BaseModel):
    origin: str
    destination: str
    carrier: str
    transit_days: int
    quantity: int
    total_cost: float
    weather_risk_score: float = 0.0
    traffic_risk_score: float = 0.0

class ShipmentOut(BaseModel):
    id: int
    tracking_number: str
    origin: str
    destination: str
    carrier: str
    transit_days: int
    quantity: int
    total_cost: float
    weather_risk_score: float
    traffic_risk_score: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class SupplierCreate(BaseModel):
    name: str
    location: str
    reliability_score: float = 0.95
    avg_lead_time_days: int = 7
    cost_per_unit: float = 50.0
    contact_email: Optional[str] = None

class SupplierOut(BaseModel):
    id: int
    name: str
    location: str
    reliability_score: float
    avg_lead_time_days: int
    cost_per_unit: float
    contact_email: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
