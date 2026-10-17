
from models.model_engine import load_dataset, split_dataset
from attacks.poisoning.label_flip import label_flip_attack
from detection.poison_detection import detect_poisoned_samples
from mitigation.mitigation import remove_suspicious_samples


def test_detection_returns_valid_metrics():
    X, y = load_dataset()
    X_train, _, y_train, _ = split_dataset(X, y)

    X_poisoned, y_poisoned, indices = label_flip_attack(
        X_train,
        y_train,
        poison_rate=0.10,
        random_state=42,
    )

    result = detect_poisoned_samples(
        None,
        X_poisoned,
        y_poisoned,
        actual_poison_indices=indices,
        contamination=0.10,
    )

    assert "suspicious_count" in result
    assert 0 <= result["detection_rate"] <= 1
    assert 0 <= result["false_positive_rate"] <= 1


def test_mitigation_removes_selected_samples():
    X, y = load_dataset()

    X_clean, y_clean = remove_suspicious_samples(
        X, y, [0, 1, 2]
    )

    assert len(X_clean) == len(X) - 3
    assert len(y_clean) == len(y) - 3
