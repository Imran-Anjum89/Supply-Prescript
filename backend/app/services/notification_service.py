from app.utils.logger import logger

class NotificationService:
    @staticmethod
    def notify_high_risk_flag(tracking_number: str, risk_level: str):
        logger.info(f"NOTIFICATION: Shipment {tracking_number} flagged with {risk_level} disruption risk!")

    @staticmethod
    def notify_retraining_complete(version: str, accuracy: float):
        logger.info(f"NOTIFICATION: Retraining complete for model {version} with accuracy {accuracy}")
