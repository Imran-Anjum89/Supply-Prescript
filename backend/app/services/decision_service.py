from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.recommendation import Recommendation
from app.models.decision import Decision
from app.models.shipment import Shipment
from app.schemas.decision_schema import DecisionRequest, DecisionOut

class DecisionService:
    @staticmethod
    def record_decision(db: Session, req: DecisionRequest) -> Decision:
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

        if req.action_taken == "ACCEPTED":
            shipment = db.query(Shipment).filter(Shipment.id == rec.shipment_id).first()
            if shipment:
                shipment.status = "MITIGATED"

        db.add(decision)
        db.commit()
        db.refresh(decision)
        return decision
