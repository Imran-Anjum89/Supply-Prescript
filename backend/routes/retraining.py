import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import RetrainingLog
from schemas import RetrainResponse, RetrainingLogOut, ModelStatusOut
from retrain import execute_model_retraining

router = APIRouter(tags=["Model Retraining"])

@router.post("/retrain", response_model=RetrainResponse)
def trigger_retrain(db: Session = Depends(get_db)):
    log_entry = execute_model_retraining(db)
    return RetrainResponse(
        message="Automated model retraining completed successfully",
        retraining_log=RetrainingLogOut.model_validate(log_entry)
    )

@router.get("/retrain/logs", response_model=List[RetrainingLogOut])
def get_retrain_logs(db: Session = Depends(get_db)):
    logs = db.query(RetrainingLog).order_by(RetrainingLog.trained_at.desc()).all()
    return logs

@router.get("/model/evaluation", response_model=ModelStatusOut)
def get_model_evaluation(db: Session = Depends(get_db)):
    latest_log = db.query(RetrainingLog).order_by(RetrainingLog.trained_at.desc()).first()
    if latest_log:
        return ModelStatusOut(
            model_version=latest_log.version,
            accuracy=latest_log.accuracy,
            mae=latest_log.mae,
            last_trained=latest_log.trained_at
        )
    return ModelStatusOut(
        model_version="v1.0",
        accuracy=0.915,
        mae=1.15,
        last_trained=datetime.datetime.utcnow()
    )
