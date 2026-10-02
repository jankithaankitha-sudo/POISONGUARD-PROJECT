import numpy as np
from sklearn.ensemble import IsolationForest


def detect_poisoned_samples(
    model,
    X,
    y,
    contamination=0.10
):

    detector = IsolationForest(
        contamination=contamination,
        random_state=42
    )

    predictions = model.predict(X)

    anomaly_labels = detector.fit_predict(X)

    suspicious_indices = np.where(
        anomaly_labels == -1
    )[0]

    return {
        "suspicious_count": int(
            len(suspicious_indices)
        ),
        "suspicious_indices":
            suspicious_indices.tolist(),
        "total_samples": int(len(y)),
        "detection_method":
            "Isolation Forest",
        "contamination": contamination
    }