import numpy as np


def label_flip_attack(
    X,
    y,
    poison_rate=0.10,
    random_state=42
):

    X_poisoned = X.copy()
    y_poisoned = y.copy()

    rng = np.random.default_rng(random_state)

    number_to_poison = int(
        len(y) * poison_rate
    )

    indices = rng.choice(
        len(y),
        size=number_to_poison,
        replace=False
    )

    unique_labels = np.unique(y)

    for index in indices:

        current_label = y_poisoned[index]

        possible_labels = [
            label
            for label in unique_labels
            if label != current_label
        ]

        y_poisoned[index] = rng.choice(
            possible_labels
        )

    return X_poisoned, y_poisoned, indices