import os
import joblib
import pandas as pd
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ml", "model.pkl")

def get_loaded_model():
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            return None
    return None

def predict_shipment_risk(shipment):
    """
    Evaluates disruption risk and delay magnitude for a shipment.
    """
    weather_score = float(shipment.weather_risk_score or 0.0)
    traffic_score = float(shipment.traffic_risk_score or 0.0)
    transit_days = float(shipment.transit_days or 10)
    carrier = shipment.carrier or "Maersk Line"
    
    carrier_map = {
        "Maersk Line": 1,
        "DHL Express": 2,
        "FedEx Supply Chain": 3,
        "OceanNet Logistics": 4,
        "Global Freight Air": 5
    }
    carrier_code = carrier_map.get(carrier, 1)
    
    model = get_loaded_model()
    
    if model is not None:
        try:
            input_df = pd.DataFrame([{
                'transit_days': transit_days,
                'quantity': float(shipment.quantity or 500),
                'total_cost': float(shipment.total_cost or 4500),
                'weather_risk_score': weather_score,
                'traffic_risk_score': traffic_score,
                'carrier_code': carrier_code
            }])
            probs = model.predict_proba(input_df)[0]
            delay_prob = float(probs[1]) if len(probs) > 1 else float(probs[0])
        except Exception:
            delay_prob = float(min(1.0, max(0.05, (weather_score * 0.45) + (traffic_score * 0.45) + (transit_days / 60.0))))
    else:
        delay_prob = float(min(1.0, max(0.05, (weather_score * 0.45) + (traffic_score * 0.45) + (transit_days / 60.0))))

    # Predict delay days based on probability and planned transit days
    predicted_delay_days = round(delay_prob * (transit_days * 0.35) + (weather_score * 3.0), 1)

    # Determine risk level
    if delay_prob < 0.25:
        risk_level = "LOW"
    elif delay_prob < 0.50:
        risk_level = "MEDIUM"
    elif delay_prob < 0.75:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    # Calculate risk feature contributions
    total_raw = (weather_score * 100) + (traffic_score * 100) + (transit_days * 1.5) + 10.0
    w_pct = round(((weather_score * 100) / total_raw) * 100, 1)
    t_pct = round(((traffic_score * 100) / total_raw) * 100, 1)
    d_pct = round(((transit_days * 1.5) / total_raw) * 100, 1)
    c_pct = round((10.0 / total_raw) * 100, 1)

    feature_contributions = {
        "Weather Impact Index": f"+{w_pct}%",
        "Port Traffic Congestion": f"+{t_pct}%",
        "Transit Duration Factor": f"+{d_pct}%",
        "Carrier Latency Variance": f"+{c_pct}%"
    }

    return {
        "delay_probability": round(delay_prob, 3),
        "predicted_delay_days": predicted_delay_days,
        "risk_level": risk_level,
        "feature_contributions": feature_contributions,
        "model_version": "v1.0"
    }
