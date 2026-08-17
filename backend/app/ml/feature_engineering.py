import pandas as pd
from app.ml.preprocess import CARRIER_MAP, clean_data

def extract_feature_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms cleaned DataFrame into numerical feature matrix for XGBoost / ML models.
    """
    df = clean_data(df)
    X = pd.DataFrame()
    X['transit_days'] = df['transit_days']
    X['quantity'] = df['quantity']
    X['total_cost'] = df['total_cost']
    X['weather_risk_score'] = df['weather_risk_score']
    X['traffic_risk_score'] = df['traffic_risk_score']
    X['supplier_reliability'] = df['supplier_reliability']
    X['carrier_code'] = df['carrier'].map(lambda c: CARRIER_MAP.get(c, 1))
    
    # Derived composite risk interaction feature
    X['combined_risk_index'] = (X['weather_risk_score'] * 0.5) + (X['traffic_risk_score'] * 0.5)
    return X
