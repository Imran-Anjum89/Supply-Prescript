import pandas as pd

CARRIER_MAP = {
    "Maersk Line": 1,
    "DHL Express": 2,
    "FedEx Supply Chain": 3,
    "OceanNet Logistics": 4,
    "Global Freight Air": 5
}

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw supply chain dataset, filling missing values and ensuring correct data types.
    """
    df = df.copy()
    df['transit_days'] = df['transit_days'].fillna(14).astype(float)
    df['quantity'] = df['quantity'].fillna(500).astype(float)
    df['total_cost'] = df['total_cost'].fillna(4500.0).astype(float)
    df['weather_risk_score'] = df['weather_risk_score'].fillna(0.0).astype(float)
    df['traffic_risk_score'] = df['traffic_risk_score'].fillna(0.0).astype(float)
    df['supplier_reliability'] = df.get('supplier_reliability', pd.Series(0.95, index=df.index)).fillna(0.95).astype(float)
    return df
