import pandas as pd


TARGET_COLUMN = "delayed"


def create_features(df):
    df = df.copy()

    # Remove columns that should not be used for prediction
    columns_to_drop = [
        "tracking_number",
        "actual_delay_days"
    ]

    df.drop(
        columns=[col for col in columns_to_drop if col in df.columns],
        inplace=True
    )

    # Create useful risk-related features
    df["total_risk_score"] = (
        df["weather_risk_score"] +
        df["traffic_risk_score"]
    ) / 2

    df["cost_per_quantity"] = (
        df["total_cost"] /
        df["quantity"].replace(0, 1)
    )

    return df


if __name__ == "__main__":
    df = pd.read_csv("dataset/supply_chain_data.csv")

    df = create_features(df)

    print("Feature engineering completed successfully")
    print("Shape:", df.shape)
    print("\nFeatures:")
    print(df.columns.tolist())