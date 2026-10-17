import os
import pandas as pd

from models.model_engine import (
    load_dataset,
    split_dataset,
    train_model,
    evaluate_model,
)
from attacks.poisoning.label_flip import label_flip_attack
from detection.poison_detection import detect_poisoned_samples
from mitigation.mitigation import remove_suspicious_samples


def run_mitigation_evaluation():
    print("\n=== PoisonGuard Week 6 Mitigation Evaluation ===")

    X, y = load_dataset()
    X_train, X_test, y_train, y_test = split_dataset(X, y)

    # Train baseline on clean data
    baseline_model = train_model(X_train, y_train)
    baseline_results = evaluate_model(
        baseline_model, X_test, y_test
    )

    # Simulate label-flipping poisoning
    X_poisoned, y_poisoned, poison_indices = label_flip_attack(
        X_train,
        y_train,
        poison_rate=0.10,
        random_state=42,
    )

    poisoned_model = train_model(X_poisoned, y_poisoned)
    poisoned_results = evaluate_model(
        poisoned_model, X_test, y_test
    )

    # Detect suspicious samples
    detection = detect_poisoned_samples(
        baseline_model,
        X_poisoned,
        y_poisoned,
        actual_poison_indices=poison_indices,
        contamination=0.10,
    )

    suspicious_indices = detection["suspicious_indices"]

    # Remove suspicious samples and retrain
    X_cleaned, y_cleaned = remove_suspicious_samples(
        X_poisoned,
        y_poisoned,
        suspicious_indices,
    )

    final_model = train_model(X_cleaned, y_cleaned)
    final_results = evaluate_model(
        final_model, X_test, y_test
    )

    rows = []
    for name, metrics in [
        ("Baseline", baseline_results),
        ("Poisoned", poisoned_results),
        ("Mitigated", final_results),
    ]:
        rows.append({
            "model": name,
            "accuracy": metrics["accuracy"],
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "f1_score": metrics["f1_score"],
        })

    os.makedirs("reports/results", exist_ok=True)
    output_file = (
        "reports/results/week6_mitigation_results.csv"
    )

    pd.DataFrame(rows).to_csv(output_file, index=False)

    print("\nDetection summary:")
    print("Actual poisoned samples:", detection["actual_poisoned"])
    print("Suspicious samples:", detection["suspicious_count"])
    print("True positives:", detection["true_positives"])
    print("False positives:", detection["false_positives"])
    print("False negatives:", detection["false_negatives"])
    print("Detection rate:", detection["detection_rate"])
    print("False-positive rate:", detection["false_positive_rate"])

    print("\nModel comparison:")
    print(pd.DataFrame(rows).to_string(index=False))
    print("\nSaved:", output_file)


if __name__ == "__main__":
    run_mitigation_evaluation()