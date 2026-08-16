from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.retraining_log import RetrainingLog
from app.services.retraining_service import RetrainingService
from app.services.evaluation_service import EvaluationService

router = APIRouter(tags=["Retraining & Model Evaluation"])

@router.post("/retrain")
def trigger_retrain(db: Session = Depends(get_db)):
    log_entry = RetrainingService.execute_retraining(db)
    return {
        "message": "Automated XGBoost model retraining completed",
        "retraining_log": log_entry
    }

@router.get("/retrain/logs")
def get_retrain_logs(db: Session = Depends(get_db)):
    return db.query(RetrainingLog).order_by(RetrainingLog.trained_at.desc()).all()

@router.get("/model/evaluation")
def get_model_evaluation(db: Session = Depends(get_db)):
    return EvaluationService.get_active_model_status(db)
