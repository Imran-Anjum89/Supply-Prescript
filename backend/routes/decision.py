from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Recommendation, Decision, Shipment
from schemas import DecisionRequest, DecisionOut

router = APIRouter(tags=["Decisions"])

@router.post("/decision", response_model=DecisionOut)
def record_decision(req: DecisionRequest, db: Session = Depends(get_db)):
    rec = db.query(Recommendation).filter(Recommendation.id == req.recommendation_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    rec.status = req.action_taken

    decision = Decision(
        recommendation_id=rec.id,
        shipment_id=rec.shipment_id,
        action_taken=req.action_taken,
        override_reason=req.override_reason
    )

    # Update shipment status if strategy was accepted
    if req.action_taken == "ACCEPTED":
        shipment = db.query(Shipment).filter(Shipment.id == rec.shipment_id).first()
        if shipment:
            shipment.status = "MITIGATED"

    db.add(decision)
    db.commit()
    db.refresh(decision)
    return decision

@router.get("/history")
def get_decision_history(limit: int = 50, db: Session = Depends(get_db)):
    decisions = db.query(Decision).order_by(Decision.timestamp.desc()).limit(limit).all()
    
    res = []
    for d in decisions:
        rec = db.query(Recommendation).filter(Recommendation.id == d.recommendation_id).first()
        shipment = db.query(Shipment).filter(Shipment.id == d.shipment_id).first()
        
        res.append({
            "id": d.id,
            "shipment_id": d.shipment_id,
            "recommendation_id": d.recommendation_id,
            "tracking_number": shipment.tracking_number if shipment else "TRK-UNKNOWN",
            "action_taken": d.action_taken,
            "override_reason": d.override_reason,
            "suggested_action": rec.suggested_action if rec else "N/A",
            "time_saved_days": rec.time_saved_days if rec else 0.0,
            "estimated_extra_cost": rec.estimated_extra_cost if rec else 0.0,
            "roi_score": rec.roi_score if rec else 1.0,
            "timestamp": d.timestamp
        })
    return res
