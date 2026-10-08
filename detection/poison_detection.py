import numpy as np
from sklearn.ensemble import IsolationForest


def detect_poisoned_samples(
    model,
    X,
    y,
    actual_poison_indices=None,
    contamination=0.10
):

    detector = IsolationForest(
        contamination=contamination,
        random_state=42
    )

    anomaly_labels = detector.fit_predict(X)

    suspicious_indices = np.where(
        anomaly_labels == -1
    )[0]

    result = {
        "suspicious_count": int(len(suspicious_indices)),
        "suspicious_indices": suspicious_indices.tolist(),
        "total_samples": int(len(y)),
        "detection_method": "Isolation Forest",
        "contamination": contamination
    }

    if actual_poison_indices is not None:

        actual_poison_set = set(
            actual_poison_indices
        )

        detected_set = set(
            suspicious_indices.tolist()
        )

        true_positives = len(
            actual_poison_set & detected_set
        )

        false_positives = len(
            detected_set - actual_poison_set
        )

        false_negatives = len(
            actual_poison_set - detected_set
        )

        detection_rate = (
            true_positives / len(actual_poison_set)
            if len(actual_poison_set) > 0
            else 0
        )

        clean_samples = (
            len(y) - len(actual_poison_set)
        )

        false_positive_rate = (
            false_positives / clean_samples
            if clean_samples > 0
            else 0
        )

        result.update({

            "actual_poisoned":
                len(actual_poison_set),

            "true_positives":
                int(true_positives),

            "false_positives":
                int(false_positives),

            "false_negatives":
                int(false_negatives),

            "detection_rate":
                round(float(detection_rate), 4),

            "false_positive_rate":
                round(
                    float(false_positive_rate),
                    4
                )
        })

    return result