import joblib
import pandas as pd

from feature_engineering import create_features


MODEL_PATH = "ml/saved_models/model.pkl"
DATA_PATH = "dataset/supply_chain_data.csv"


def predict_delay(shipment_data):

    # Load trained model
    model = joblib.load(MODEL_PATH)

    # Convert input to DataFrame
    df = pd.DataFrame([shipment_data])

    # Apply same feature engineering used during training
    df = create_features(df)

    # Remove target column if present
    df = df.drop(columns=["delayed"], errors="ignore")

    # Load original dataset for categorical mappings
    training_data = pd.read_csv(DATA_PATH)

    # Create mappings
    origin_mapping = {
        value: index
        for index, value in enumerate(
            training_data["origin"].unique()
        )
    }

    destination_mapping = {
        value: index
        for index, value in enumerate(
            training_data["destination"].unique()
        )
    }

    carrier_mapping = {
        value: index
        for index, value in enumerate(
            training_data["carrier"].unique()
        )
    }

    # Encode categorical columns
    df["origin"] = df["origin"].map(origin_mapping)
    df["destination"] = df["destination"].map(destination_mapping)
    df["carrier"] = df["carrier"].map(carrier_mapping)

    # Check for unknown categories
    if df[["origin", "destination", "carrier"]].isnull().any().any():
        raise ValueError(
            "Unknown origin, destination, or carrier found in input."
        )

    # Ensure feature order matches training
    feature_order = [
        "origin",
        "destination",
        "carrier",
        "transit_days",
        "quantity",
        "total_cost",
        "weather_risk_score",
        "traffic_risk_score",
        "supplier_reliability",
        "total_risk_score",
        "cost_per_quantity"
    ]

    df = df[feature_order]

    # Make prediction
    prediction = model.predict(df)[0]

    # Get probability
    probability = model.predict_proba(df)[0][1]

    # Convert prediction to readable result
    if prediction == 1:
        result = "Delayed"
    else:
        result = "Not Delayed"

    return result, probability


if __name__ == "__main__":

    sample_shipment = {
    "tracking_number": "TRK-TEST-001",
    "origin": "Shanghai Port (CN)",
    "destination": "Port of Los Angeles (US)",
    "carrier": "Maersk Line",
    "transit_days": 12,
    "quantity": 500,
    "total_cost": 25000,
    "weather_risk_score": 0.45,
    "traffic_risk_score": 0.60,
    "supplier_reliability": 0.80
}

    result, probability = predict_delay(sample_shipment)

    print("\nPrediction Result")
    print("=================")
    print("Shipment Status:", result)
    print(f"Delay Probability: {probability:.2%}")