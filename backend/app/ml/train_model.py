import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
backend_path = os.path.join(PROJECT_ROOT, "backend")

if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from app.ml.feature_engineering import extract_feature_matrix
from app.ml.evaluate_model import evaluate_model_performance
from app.ml.generate_raw import generate_raw_dataset

try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    from sklearn.ensemble import RandomForestClassifier as XGBClassifier
    HAS_XGBOOST = False

RAW_DATASET_PATH = os.path.join(PROJECT_ROOT, "dataset", "raw", "supply_chain.csv")
SAVED_MODELS_DIR = os.path.join(os.path.dirname(__file__), "saved_models")

def load_data():
    if not os.path.exists(RAW_DATASET_PATH):
        print(f"Dataset missing at {RAW_DATASET_PATH}. Generating new dataset...")
        return generate_raw_dataset(num_records=1200, output_path=RAW_DATASET_PATH)
    return pd.read_csv(RAW_DATASET_PATH)

def train_and_save_model():
    df = load_data()
    X = extract_feature_matrix(df)
    y = df['delayed']
    y_days = df.get('actual_delay_days', None)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    if HAS_XGBOOST:
        model = XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.08, random_state=42, eval_metric='logloss')
    else:
        model = XGBClassifier(n_estimators=100, max_depth=5, random_state=42)

    model.fit(X_train, y_train)

    metrics = evaluate_model_performance(model, X_test, y_test, y_days.iloc[X_test.index] if y_days is not None else None)

    os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
    v1_path = os.path.join(SAVED_MODELS_DIR, "v1.pkl")
    latest_path = os.path.join(SAVED_MODELS_DIR, "latest.pkl")
    
    joblib.dump(model, v1_path)
    joblib.dump(model, latest_path)
    
    root_model_path = os.path.join(PROJECT_ROOT, "ml", "model.pkl")
    os.makedirs(os.path.dirname(root_model_path), exist_ok=True)
    joblib.dump(model, root_model_path)

    print(f"XGBoost Model successfully trained!")
    print(f"Metrics: {metrics}")
    print(f"Saved artifacts to {latest_path} and {v1_path}")
    return model, metrics

if __name__ == "__main__":
    train_and_save_model()
