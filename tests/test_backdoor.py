from models.model_engine import load_dataset
from attacks.backdoor.feature_trigger import backdoor_attack


def test_backdoor_attack():

    X, y = load_dataset()

    (
        X_backdoor,
        y_backdoor,
        indices,
        trigger_feature,
        trigger_value
    ) = backdoor_attack(
        X,
        y,
        poison_rate=0.05,
        target_label=1,
        random_state=42
    )

    assert len(indices) > 0
    assert len(X_backdoor) == len(X)
    assert len(y_backdoor) == len(y)
    assert trigger_feature >= 0