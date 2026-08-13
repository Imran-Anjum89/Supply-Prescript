import datetime
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(Integer, ForeignKey("decisions.id"), nullable=False)
    actual_delay_days = Column(Float, nullable=False)
    actual_extra_cost = Column(Float, default=0.0)
    outcome_rating = Column(Integer, default=5)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    decision = relationship("Decision", back_populates="feedbacks")
