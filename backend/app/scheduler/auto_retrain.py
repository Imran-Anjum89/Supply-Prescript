from app.database import SessionLocal
from app.services.retraining_service import RetrainingService
from app.utils.logger import logger

def check_and_trigger_auto_retrain():
    db = SessionLocal()
    try:
        logger.info("Scheduler: Checking closed-loop feedback threshold for automated retraining...")
        log_entry = RetrainingService.execute_retraining(db)
        logger.info(f"Scheduler: Automated retraining completed successfully. Version: {log_entry.version}")
    except Exception as e:
        logger.error(f"Scheduler: Retraining check failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_and_trigger_auto_retrain()
