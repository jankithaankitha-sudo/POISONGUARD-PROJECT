
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    VotingClassifier
)

import joblib
import os


MODEL_DIR = "models/trained_models"
os.makedirs(MODEL_DIR, exist_ok=True)


def create_robust_model():

    # Model 1: Random Forest
    random_forest = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    # Model 2: Extra Trees
    extra_trees = ExtraTreesClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    # Model 3: Gradient Boosting
    gradient_boosting = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        random_state=42
    )

    # Combine models using soft voting
    robust_model = VotingClassifier(
        estimators=[
            ("random_forest", random_forest),
            ("extra_trees", extra_trees),
            ("gradient_boosting", gradient_boosting)
        ],
        voting="soft"
    )

    return robust_model


def train_robust_model(X_train, y_train):

    model = create_robust_model()

    model.fit(X_train, y_train)

    return model


def save_robust_model(model):

    path = os.path.join(
        MODEL_DIR,
        "robust_ensemble_model.pkl"
    )

    joblib.dump(model, path)

    return path


def load_robust_model():

    path = os.path.join(
        MODEL_DIR,
        "robust_ensemble_model.pkl"
    )

    return joblib.load(path)
