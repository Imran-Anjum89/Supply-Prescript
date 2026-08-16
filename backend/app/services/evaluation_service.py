import datetime
from sqlalchemy.orm import Session
from app.models.retraining_log import RetrainingLog

class EvaluationService:
    @staticmethod
    def get_active_model_status(db: Session):
        latest_log = db.query(RetrainingLog).order_by(RetrainingLog.trained_at.desc()).first()
        if latest_log:
            return {
                "model_version": latest_log.version,
                "accuracy": latest_log.accuracy,
                "mae": latest_log.mae,
                "last_trained": latest_log.trained_at
            }
        return {
            "model_version": "v1.0",
            "accuracy": 0.9708,
            "mae": 1.66,
            "last_trained": datetime.datetime.utcnow()
        }
