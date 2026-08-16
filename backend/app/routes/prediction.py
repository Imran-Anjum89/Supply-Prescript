from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.prediction import Prediction
from app.schemas.prediction_schema import PredictRequest, PredictionOut
from app.services.prediction_service import PredictionService

router = APIRouter(tags=["Prediction"])

@router.post("/predict", response_model=PredictionOut)
def predict_shipment(req: PredictRequest, db: Session = Depends(get_db)):
    return PredictionService.create_prediction(db, req.shipment_id)

@router.get("/predictions/shipment/{shipment_id}", response_model=List[PredictionOut])
def get_predictions(shipment_id: int, db: Session = Depends(get_db)):
    return db.query(Prediction).filter(Prediction.shipment_id == shipment_id).order_by(Prediction.created_at.desc()).all()
