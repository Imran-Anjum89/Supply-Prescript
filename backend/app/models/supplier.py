import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    reliability_score = Column(Float, default=0.95)
    avg_lead_time_days = Column(Integer, default=7)
    cost_per_unit = Column(Float, default=50.0)
    contact_email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
