import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class RetrainingLog(Base):
    __tablename__ = "retraining_logs"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, nullable=False)
    accuracy = Column(Float, nullable=False)
    mae = Column(Float, nullable=False)
    records_used = Column(Integer, nullable=False)
    status = Column(String, default="SUCCESS")
    trained_at = Column(DateTime, default=datetime.datetime.utcnow)
