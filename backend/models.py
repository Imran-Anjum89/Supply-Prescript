from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func

from database import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(String, unique=True, nullable=False)
    supplier = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    status = Column(String, default="Pending")
    delay_probability = Column(Float, default=0.0)
    risk_level = Column(String, default="Low")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    reliability_score = Column(Float, default=0.0)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(String, nullable=False)
    delay_probability = Column(Float)
    predicted_delay_days = Column(Integer)
    risk_level = Column(String)


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(String, nullable=False)
    recommendation = Column(String)
    accepted = Column(Boolean, default=False)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(String, nullable=False)
    actual_delay_days = Column(Integer)
    comments = Column(String)
