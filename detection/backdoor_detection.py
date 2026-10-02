import numpy as np


def detect_backdoor(
    model,
    X,
    trigger_feature,
    trigger_value,
    target_label=1
):

    X_triggered = X.copy()

    X_triggered[
        :,
        trigger_feature
    ] = trigger_value

    normal_predictions = model.predict(X)

    triggered_predictions = model.predict(
        X_triggered
    )

    changed = (
        normal_predictions
        != triggered_predictions
    )

    target_predictions = (
        triggered_predictions
        == target_label
    )

    suspicious_count = np.sum(
        changed & target_predictions
    )

    total = len(X)

    attack_success_rate = (
        suspicious_count / total
        if total > 0
        else 0
    )

    return {
        "trigger_feature": int(trigger_feature),
        "trigger_value": float(trigger_value),
        "suspicious_count": int(
            suspicious_count
        ),
        "attack_success_rate": round(
            float(attack_success_rate),
            4
        )
    }