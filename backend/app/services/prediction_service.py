from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.shipment import Shipment
from app.models.prediction import Prediction
from app.ml.predict_model import predict_disruption_risk

class PredictionService:
    @staticmethod
    def create_prediction(db: Session, shipment_id: int) -> Prediction:
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")

        risk_res = predict_disruption_risk(shipment)

        prediction = Prediction(
            shipment_id=shipment.id,
            delay_probability=risk_res["delay_probability"],
            predicted_delay_days=risk_res["predicted_delay_days"],
            risk_level=risk_res["risk_level"],
            feature_contributions=risk_res["feature_contributions"],
            model_version=risk_res["model_version"]
        )
        db.add(prediction)

        if risk_res["risk_level"] in ["HIGH", "CRITICAL"]:
            shipment.status = "DELAY_RISK"

        db.commit()
        db.refresh(prediction)
        return prediction
