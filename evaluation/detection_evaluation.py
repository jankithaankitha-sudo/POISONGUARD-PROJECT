
import os
import pandas as pd

from models.model_engine import (
    load_dataset,
    split_dataset,
    train_model
)
from attacks.poisoning.label_flip import label_flip_attack
from detection.poison_detection import detect_poisoned_samples


def run_detection_experiment():
    print("\n=== PoisonGuard Week 6 ===")
    print("Detection Evaluation Experiment\n")

    # Load and split the dataset
    X, y = load_dataset()

    X_train, X_test, y_train, y_test = split_dataset(X, y)

    # Train a reference model using clean training data
    baseline_model = train_model(X_train, y_train)

    # Simulate a 10% label-flipping attack
    X_poisoned, y_poisoned, poison_indices = label_flip_attack(
        X_train,
        y_train,
        poison_rate=0.10,
        random_state=42
    )

    print("Training samples:", len(y_train))
    print("Actual poisoned samples:", len(poison_indices))

    # Test different Isolation Forest contamination settings
    contamination_values = [0.05, 0.10, 0.15, 0.20]
    results = []

    for contamination in contamination_values:

        # Existing detector identifies feature anomalies
        isolation_result = detect_poisoned_samples(
            baseline_model,
            X_poisoned,
            y_poisoned,
            actual_poison_indices=poison_indices,
            contamination=contamination
        )

        # Compare observed labels against clean-model predictions
        predictions = baseline_model.predict(X_poisoned)
        disagreement_indices = set(
            (predictions != y_poisoned).nonzero()[0].tolist()
        )

        actual_poison_set = set(poison_indices.tolist())

        true_positives = len(
            disagreement_indices & actual_poison_set
        )
        false_positives = len(
            disagreement_indices - actual_poison_set
        )
        false_negatives = len(
            actual_poison_set - disagreement_indices
        )

        detection_rate = (
            true_positives / len(actual_poison_set)
            if actual_poison_set else 0.0
        )

        clean_count = len(y_train) - len(actual_poison_set)

        false_positive_rate = (
            false_positives / clean_count
            if clean_count else 0.0
        )

        results.append({
            "contamination": contamination,
            "actual_poisoned": len(actual_poison_set),
            "isolation_suspicious": isolation_result[
                "suspicious_count"
            ],
            "isolation_detection_rate": isolation_result[
                "detection_rate"
            ],
            "label_disagreements": len(disagreement_indices),
            "label_true_positives": true_positives,
            "label_false_positives": false_positives,
            "label_false_negatives": false_negatives,
            "label_detection_rate": round(detection_rate, 4),
            "label_false_positive_rate": round(
                false_positive_rate, 4
            )
        })

    # Save experiment results
    output_dir = "reports/results"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        "detection_experiment_results.csv"
    )

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)

    print("\n=== Detection Comparison ===")
    print(results_df.to_string(index=False))
    print("\nResults saved to:", output_file)


if __name__ == "__main__":
    run_detection_experiment()
