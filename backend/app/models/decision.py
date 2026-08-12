import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=False)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    action_taken = Column(String, nullable=False) # ACCEPTED, OVERRIDDEN
    override_reason = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    recommendation = relationship("Recommendation", back_populates="decisions")
    shipment = relationship("Shipment", back_populates="decisions")
    feedbacks = relationship("Feedback", back_populates="decision", cascade="all, delete-orphan")
