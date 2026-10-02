import numpy as np


def remove_suspicious_samples(
    X,
    y,
    suspicious_indices
):

    suspicious_set = set(
        suspicious_indices
    )

    keep_indices = [
        i
        for i in range(len(X))
        if i not in suspicious_set
    ]

    X_clean = X[keep_indices]
    y_clean = y[keep_indices]

    return X_clean, y_clean