import pandas as pd
import os

RAW_PATH = "dataset/raw/supply_chain.csv"
OUTPUT_PATH = "dataset/supply_chain_data.csv"


def generate_raw_dataset():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"Raw dataset not found: {RAW_PATH}")

    df = pd.read_csv(RAW_PATH)

    print("Raw dataset loaded successfully")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print(df.head())

    os.makedirs("dataset", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nProcessed dataset saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_raw_dataset()