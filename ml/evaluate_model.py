import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from feature_engineering import create_features


DATA_PATH = "dataset/supply_chain_data.csv"
MODEL_PATH = "ml/saved_models/model.pkl"


def evaluate_model():

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

    # Same split used during training
    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Load trained model
    model = joblib.load(MODEL_PATH)

    # Predict
    predictions = model.predict(X_test)

    # Metrics
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    print("Model Evaluation")
    print("================")
    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))


if __name__ == "__main__":
    evaluate_model()