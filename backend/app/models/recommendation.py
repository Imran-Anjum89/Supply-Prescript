import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    suggested_action = Column(String, nullable=False)
    expedited_carrier = Column(String, nullable=True)
    estimated_extra_cost = Column(Float, nullable=False)
    time_saved_days = Column(Float, nullable=False)
    roi_score = Column(Float, nullable=False)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    shipment = relationship("Shipment", back_populates="recommendations")
    decisions = relationship("Decision", back_populates="recommendation", cascade="all, delete-orphan")
