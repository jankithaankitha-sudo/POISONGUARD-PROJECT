
import numpy as np


def remove_suspicious_samples(X, y, suspicious_indices):
    """Remove selected suspicious samples from training data."""

    X = np.asarray(X)
    y = np.asarray(y)

    if len(X) != len(y):
        raise ValueError("X and y must have equal sample counts.")

    if len(X) == 0:
        raise ValueError("Cannot mitigate an empty dataset.")

    indices = set()

    for index in suspicious_indices:
        if not isinstance(index, (int, np.integer)):
            raise ValueError("Sample indices must be integers.")

        if index < 0 or index >= len(X):
            raise ValueError(f"Invalid sample index: {index}")

        indices.add(int(index))

    if len(indices) >= len(X):
        raise ValueError("Cannot remove every training sample.")

    keep_mask = np.ones(len(X), dtype=bool)

    if indices:
        keep_mask[list(indices)] = False

    return X[keep_mask], y[keep_mask]


def mitigation_summary(original_count, suspicious_indices, remaining_count):
    """Summarize the filtering operation."""

    removed_count = len(set(suspicious_indices))

    return {
        "original_samples": int(original_count),
        "suspicious_samples_removed": int(removed_count),
        "remaining_samples": int(remaining_count),
        "removal_rate": round(removed_count / original_count, 4)
        if original_count else 0.0
    }
