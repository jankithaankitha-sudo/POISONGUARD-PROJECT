
import numpy as np
import pytest

from mitigation.mitigation import (
    remove_suspicious_samples,
    mitigation_summary,
)


def test_remove_suspicious_sample():
    X = np.array([[1, 2], [3, 4], [5, 6]])
    y = np.array([0, 1, 0])

    X_clean, y_clean = remove_suspicious_samples(X, y, [1])

    assert len(X_clean) == 2
    assert np.array_equal(y_clean, [0, 0])


def test_no_suspicious_samples():
    X = np.array([[1, 2], [3, 4]])
    y = np.array([0, 1])

    X_clean, y_clean = remove_suspicious_samples(X, y, [])

    assert len(X_clean) == 2
    assert np.array_equal(y_clean, y)


def test_invalid_index():
    X = np.array([[1, 2], [3, 4]])
    y = np.array([0, 1])

    with pytest.raises(ValueError):
        remove_suspicious_samples(X, y, [10])


def test_cannot_remove_every_sample():
    X = np.array([[1, 2], [3, 4]])
    y = np.array([0, 1])

    with pytest.raises(ValueError):
        remove_suspicious_samples(X, y, [0, 1])


def test_mitigation_summary():
    result = mitigation_summary(10, [1, 2], 8)

    assert result["original_samples"] == 10
    assert result["suspicious_samples_removed"] == 2
    assert result["remaining_samples"] == 8
    assert result["removal_rate"] == 0.2
