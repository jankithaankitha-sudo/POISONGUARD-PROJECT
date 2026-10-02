import numpy as np


def backdoor_attack(
    X,
    y,
    poison_rate=0.05,
    target_label=1,
    random_state=42
):

    X_poisoned = X.copy()
    y_poisoned = y.copy()

    rng = np.random.default_rng(random_state)

    number_to_poison = int(
        len(X) * poison_rate
    )

    indices = rng.choice(
        len(X),
        size=number_to_poison,
        replace=False
    )

    # Use feature 0 as the demonstration trigger.
    trigger_feature = 0

    trigger_value = np.percentile(
        X[:, trigger_feature],
        99
    )

    for index in indices:

        X_poisoned[
            index,
            trigger_feature
        ] = trigger_value

        y_poisoned[index] = target_label

    return (
        X_poisoned,
        y_poisoned,
        indices,
        trigger_feature,
        trigger_value
    )