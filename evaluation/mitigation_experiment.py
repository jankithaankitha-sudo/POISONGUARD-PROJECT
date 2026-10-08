from models.model_engine import (
    load_dataset,
    split_dataset,
    train_model,
    evaluate_model
)

from attacks.poisoning.label_flip import label_flip_attack
from detection.poison_detection import detect_poisoned_samples
from mitigation.mitigation import remove_suspicious_samples


def run_mitigation_experiment():

    X, y = load_dataset()

    X_train, X_test, y_train, y_test = split_dataset(
        X,
        y
    )

    print("\n========================================")
    print(" PoisonGuard Mitigation Experiment")
    print("========================================")

    # Baseline model
    baseline_model = train_model(
        X_train,
        y_train
    )

    baseline_results = evaluate_model(
        baseline_model,
        X_test,
        y_test
    )

    # Create poisoned dataset
    X_poisoned, y_poisoned, poison_indices = label_flip_attack(
        X_train,
        y_train,
        poison_rate=0.10,
        random_state=42
    )

    # Train poisoned model
    poisoned_model = train_model(
        X_poisoned,
        y_poisoned
    )

    poisoned_results = evaluate_model(
        poisoned_model,
        X_test,
        y_test
    )

    # Detect suspicious samples
    detection = detect_poisoned_samples(
        poisoned_model,
        X_poisoned,
        y_poisoned,
        actual_poison_indices=poison_indices
    )

    # Remove suspicious samples
    X_clean, y_clean = remove_suspicious_samples(
        X_poisoned,
        y_poisoned,
        detection["suspicious_indices"]
    )

    # Retrain final model
    final_model = train_model(
        X_clean,
        y_clean
    )

    final_results = evaluate_model(
        final_model,
        X_test,
        y_test
    )

    print("\n----------------------------------------")
    print("Mitigation Results")
    print("----------------------------------------")
    print(f"Baseline Accuracy  : {baseline_results['accuracy']}")
    print(f"Poisoned Accuracy  : {poisoned_results['accuracy']}")
    print(f"Actual Poisoned    : {detection['actual_poisoned']}")
    print(f"Suspicious Samples : {detection['suspicious_count']}")
    print(f"Detection Rate     : {detection['detection_rate']}")
    print(f"False Positive Rate: {detection['false_positive_rate']}")
    print(f"Final Accuracy     : {final_results['accuracy']}")


if __name__ == "__main__":
    run_mitigation_experiment()