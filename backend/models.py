import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="Logistics Manager")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, index=True, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    carrier = Column(String, nullable=False)
    transit_days = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_cost = Column(Float, nullable=False)
    weather_risk_score = Column(Float, default=0.0)
    traffic_risk_score = Column(Float, default=0.0)
    status = Column(String, default="IN_TRANSIT")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    predictions = relationship("Prediction", back_populates="shipment", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="shipment", cascade="all, delete-orphan")
    decisions = relationship("Decision", back_populates="shipment", cascade="all, delete-orphan")

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

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    delay_probability = Column(Float, nullable=False)
    predicted_delay_days = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    feature_contributions = Column(JSON, nullable=True)
    model_version = Column(String, default="v1.0")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    shipment = relationship("Shipment", back_populates="predictions")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    suggested_action = Column(String, nullable=False)
    expedited_carrier = Column(String, nullable=True)
    estimated_extra_cost = Column(Float, nullable=False)
    time_saved_days = Column(Float, nullable=False)
    roi_score = Column(Float, nullable=False)
    status = Column(String, default="PENDING") # PENDING, ACCEPTED, OVERRIDDEN
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    shipment = relationship("Shipment", back_populates="recommendations")
    decisions = relationship("Decision", back_populates="recommendation", cascade="all, delete-orphan")

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

class RetrainingLog(Base):
    __tablename__ = "retraining_logs"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, nullable=False)
    accuracy = Column(Float, nullable=False)
    mae = Column(Float, nullable=False)
    records_used = Column(Integer, nullable=False)
    status = Column(String, default="SUCCESS")
    trained_at = Column(DateTime, default=datetime.datetime.utcnow)
