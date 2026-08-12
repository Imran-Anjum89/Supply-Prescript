import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

from feature_engineering import create_features


DATA_PATH = "dataset/supply_chain_data.csv"
MODEL_DIR = "ml/saved_models"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")


def train_model():

    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Feature engineering
    df = create_features(df)

    # Encode categorical columns
    categorical_columns = [
        "origin",
        "destination",
        "carrier"
    ]

    for column in categorical_columns:
        encoder = LabelEncoder()
        df[column] = encoder.fit_transform(df[column])

    # Features and target
    X = df.drop("delayed", axis=1)
    y = df["delayed"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # XGBoost model
    model = XGBClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=6,
        random_state=42,
        eval_metric="logloss"
    )

    # Train
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("XGBoost Model Training Completed")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    # Create model directory
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Save model
    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved successfully: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()