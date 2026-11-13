
import os
import csv

from models.model_engine import (
    load_dataset,
    split_dataset,
    create_model,
    evaluate_model
)

from models.robust_training import (
    train_robust_model,
    save_robust_model
)

from attacks.poisoning.label_flip import label_flip_attack


POISON_RATES = [0.05, 0.10, 0.20]


def run_robust_training_experiment():

    X, y = load_dataset()

    X_train, X_test, y_train, y_test = split_dataset(
        X, y
    )

    results_data = []

    print("\n========================================")
    print(" PoisonGuard - Week 10")
    print(" Robust Training Evaluation")
    print("========================================")

    for rate in POISON_RATES:

        print(f"\nTesting poisoning rate: {rate * 100:.0f}%")

        # Generate poisoned training data
        X_poisoned, y_poisoned, poison_indices = label_flip_attack(
            X_train,
            y_train,
            poison_rate=rate,
            random_state=42
        )

        # Train baseline Random Forest
        baseline_model = create_model()

        baseline_model.fit(
            X_poisoned,
            y_poisoned
        )

        baseline_results = evaluate_model(
            baseline_model,
            X_test,
            y_test
        )

        # Train robust ensemble
        robust_model = train_robust_model(
            X_poisoned,
            y_poisoned
        )

        # Save the ensemble trained at 10% poisoning
        if rate == 0.10:
            saved_path = save_robust_model(robust_model)
            print("Robust model saved:", saved_path)

        robust_results = evaluate_model(
            robust_model,
            X_test,
            y_test
        )

        # Store comparison results
        row = {
            "poisoning_rate": int(rate * 100),
            "poisoned_samples": len(poison_indices),

            "baseline_accuracy": baseline_results["accuracy"],
            "baseline_precision": baseline_results["precision"],
            "baseline_recall": baseline_results["recall"],
            "baseline_f1": baseline_results["f1_score"],

            "robust_accuracy": robust_results["accuracy"],
            "robust_precision": robust_results["precision"],
            "robust_recall": robust_results["recall"],
            "robust_f1": robust_results["f1_score"]
        }

        results_data.append(row)

        print("\nBaseline Random Forest:")
        print("Accuracy :", baseline_results["accuracy"])
        print("Precision:", baseline_results["precision"])
        print("Recall   :", baseline_results["recall"])
        print("F1 Score :", baseline_results["f1_score"])

        print("\nRobust Ensemble:")
        print("Accuracy :", robust_results["accuracy"])
        print("Precision:", robust_results["precision"])
        print("Recall   :", robust_results["recall"])
        print("F1 Score :", robust_results["f1_score"])

    # Save experiment results
    os.makedirs("reports/results", exist_ok=True)

    output_file = "reports/results/robust_training_results.csv"

    with open(output_file, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=list(results_data[0].keys())
        )

        writer.writeheader()
        writer.writerows(results_data)

    print("\n========================================")
    print("Robust training experiment completed.")
    print("Results saved to:")
    print(output_file)
    print("========================================")


if __name__ == "__main__":
    run_robust_training_experiment()
