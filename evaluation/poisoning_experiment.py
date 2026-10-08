import os
import csv

from models.model_engine import (
    load_dataset,
    split_dataset,
    train_model,
    evaluate_model
)

from attacks.poisoning.label_flip import label_flip_attack


POISON_RATES = [0.05, 0.10, 0.20, 0.30]


def run_poisoning_experiments():

    X, y = load_dataset()

    X_train, X_test, y_train, y_test = split_dataset(
        X,
        y
    )

    results_data = []

    print("\n========================================")
    print(" PoisonGuard Poisoning Experiments")
    print("========================================")

    for rate in POISON_RATES:

        X_poisoned, y_poisoned, poison_indices = label_flip_attack(
            X_train,
            y_train,
            poison_rate=rate,
            random_state=42
        )

        model = train_model(
            X_poisoned,
            y_poisoned
        )

        results = evaluate_model(
            model,
            X_test,
            y_test
        )

        row = {
            "poisoning_rate": int(rate * 100),
            "poisoned_samples": len(poison_indices),
            "accuracy": results["accuracy"],
            "precision": results["precision"],
            "recall": results["recall"],
            "f1_score": results["f1_score"]
        }

        results_data.append(row)

        print("\n----------------------------------------")
        print(f"Poisoning Rate : {rate * 100:.0f}%")
        print(f"Poisoned Samples: {len(poison_indices)}")
        print(f"Accuracy       : {results['accuracy']}")
        print(f"Precision      : {results['precision']}")
        print(f"Recall         : {results['recall']}")
        print(f"F1 Score       : {results['f1_score']}")

    os.makedirs("reports/results", exist_ok=True)

    output_file = "reports/results/poisoning_experiment_results.csv"

    with open(output_file, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "poisoning_rate",
                "poisoned_samples",
                "accuracy",
                "precision",
                "recall",
                "f1_score"
            ]
        )

        writer.writeheader()
        writer.writerows(results_data)

    print("\n========================================")
    print("Experiment results saved to:")
    print(output_file)
    print("========================================")


if __name__ == "__main__":
    run_poisoning_experiments()