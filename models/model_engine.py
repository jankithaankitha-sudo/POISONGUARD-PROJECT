import os
import joblib

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


MODEL_DIR = "models/trained_models"
os.makedirs(MODEL_DIR, exist_ok=True)


def load_dataset():
    data = load_breast_cancer()

    X = data.data
    y = data.target

    return X, y


def split_dataset(X, y):
    return train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )


def create_model():
    return RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )


def train_model(X_train, y_train):
    model = create_model()
    model.fit(X_train, y_train)

    return model


def evaluate_model(model, X_test, y_test):

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )
    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )
    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    matrix = confusion_matrix(
        y_test,
        predictions
    )

    return {
        "accuracy": round(float(accuracy), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1_score": round(float(f1), 4),
        "confusion_matrix": matrix.tolist()
    }


def save_model(model, filename):

    path = os.path.join(
        MODEL_DIR,
        filename
    )

    joblib.dump(model, path)

    return path


def load_model(filename):

    path = os.path.join(
        MODEL_DIR,
        filename
    )

    return joblib.load(path)