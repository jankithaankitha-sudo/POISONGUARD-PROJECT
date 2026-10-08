from models.model_engine import load_dataset
from attacks.poisoning.label_flip import label_flip_attack


def test_label_flip_attack():

    X, y = load_dataset()

    X_poisoned, y_poisoned, indices = label_flip_attack(
        X,
        y,
        poison_rate=0.10,
        random_state=42
    )

    assert len(indices) > 0
    assert len(X_poisoned) == len(X)
    assert len(y_poisoned) == len(y)