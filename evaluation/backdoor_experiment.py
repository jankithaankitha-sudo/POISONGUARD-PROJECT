from models.model_engine import (
    load_dataset,
    split_dataset,
    train_model,
    evaluate_model
)

from attacks.backdoor.feature_trigger import backdoor_attack
from detection.backdoor_detection import detect_backdoor


def run_backdoor_experiment():

    X, y = load_dataset()

    X_train, X_test, y_train, y_test = split_dataset(
        X,
        y
    )

    print("\n========================================")
    print(" PoisonGuard Backdoor Experiment")
    print("========================================")

    (
        X_backdoor,
        y_backdoor,
        indices,
        trigger_feature,
        trigger_value
    ) = backdoor_attack(
        X_train,
        y_train,
        poison_rate=0.05,
        target_label=1,
        random_state=42
    )

    model = train_model(
        X_backdoor,
        y_backdoor
    )

    results = evaluate_model(
        model,
        X_test,
        y_test
    )

    detection = detect_backdoor(
        model,
        X_test,
        trigger_feature,
        trigger_value,
        target_label=1
    )

    print("\n----------------------------------------")
    print("Backdoor Attack")
    print("----------------------------------------")
    print(f"Backdoor Samples   : {len(indices)}")
    print(f"Trigger Feature    : {trigger_feature}")
    print(f"Trigger Value      : {trigger_value}")
    print(f"Accuracy           : {results['accuracy']}")
    print(f"Attack Success Rate: {detection['attack_success_rate']}")
    print(f"Suspicious Count   : {detection['suspicious_count']}")


if __name__ == "__main__":
    run_backdoor_experiment()