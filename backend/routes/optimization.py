from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Shipment, Prediction, Recommendation
from schemas import RecommendRequest, RecommendationOut
from predict import predict_shipment_risk
from optimize import solve_prescriptive_optimization

router = APIRouter(tags=["Optimization"])

@router.post("/recommend", response_model=RecommendationOut)
def generate_recommendation(req: RecommendRequest, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.id == req.shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    # Get latest prediction or run new one
    latest_pred = db.query(Prediction).filter(Prediction.shipment_id == shipment.id).order_by(Prediction.created_at.desc()).first()
    if not latest_pred:
        risk_res = predict_shipment_risk(shipment)
    else:
        risk_res = {
            "delay_probability": latest_pred.delay_probability,
            "predicted_delay_days": latest_pred.predicted_delay_days,
            "risk_level": latest_pred.risk_level
        }

    opt_res = solve_prescriptive_optimization(shipment, risk_res, req.max_budget_extra)

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

@router.get("/recommendations/shipment/{shipment_id}", response_model=List[RecommendationOut])
def get_recommendations_for_shipment(shipment_id: int, db: Session = Depends(get_db)):
    recs = db.query(Recommendation).filter(Recommendation.shipment_id == shipment_id).order_by(Recommendation.created_at.desc()).all()
    return recs
