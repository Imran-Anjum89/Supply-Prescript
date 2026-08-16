from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.decision import Decision
from app.models.recommendation import Recommendation
from app.models.shipment import Shipment

router = APIRouter(tags=["History"])

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
