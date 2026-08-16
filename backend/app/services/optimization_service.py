from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.shipment import Shipment
from app.models.prediction import Prediction
from app.models.recommendation import Recommendation
from app.ml.predict_model import predict_disruption_risk
from app.optimization.pulp_solver import solve_pulp_prescriptive_recommendation

class OptimizationService:
    @staticmethod
    def generate_recommendation(db: Session, shipment_id: int, max_budget_extra: float = 1200.0) -> Recommendation:
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")

        latest_pred = db.query(Prediction).filter(Prediction.shipment_id == shipment.id).order_by(Prediction.created_at.desc()).first()
        if not latest_pred:
            risk_res = predict_disruption_risk(shipment)
        else:
            risk_res = {
                "delay_probability": latest_pred.delay_probability,
                "predicted_delay_days": latest_pred.predicted_delay_days,
                "risk_level": latest_pred.risk_level
            }

        opt_res = solve_pulp_prescriptive_recommendation(shipment, risk_res, max_budget_extra)

        recommendation = Recommendation(
            shipment_id=shipment.id,
            suggested_action=opt_res["suggested_action"],
            expedited_carrier=opt_res["expedited_carrier"],
            estimated_extra_cost=opt_res["estimated_extra_cost"],
            time_saved_days=opt_res["time_saved_days"],
            roi_score=opt_res["roi_score"],
            status="PENDING"
        )
        db.add(recommendation)
        db.commit()
        db.refresh(recommendation)
        return recommendation
