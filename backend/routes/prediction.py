from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Shipment, Prediction
from schemas import PredictRequest, PredictionOut
from predict import predict_shipment_risk

router = APIRouter(tags=["Prediction"])

@router.post("/predict", response_model=PredictionOut)
def run_prediction(req: PredictRequest, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.id == req.shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    risk_res = predict_shipment_risk(shipment)
    
    prediction = Prediction(
        shipment_id=shipment.id,
        delay_probability=risk_res["delay_probability"],
        predicted_delay_days=risk_res["predicted_delay_days"],
        risk_level=risk_res["risk_level"],
        feature_contributions=risk_res["feature_contributions"],
        model_version=risk_res["model_version"]
    )
    db.add(prediction)
    
    # Update shipment status based on risk level
    if risk_res["risk_level"] in ["HIGH", "CRITICAL"]:
        shipment.status = "DELAY_RISK"
    
    db.commit()
    db.refresh(prediction)
    return prediction

@router.get("/predictions/shipment/{shipment_id}", response_model=List[PredictionOut])
def get_predictions_for_shipment(shipment_id: int, db: Session = Depends(get_db)):
    predictions = db.query(Prediction).filter(Prediction.shipment_id == shipment_id).order_by(Prediction.created_at.desc()).all()
    return predictions
