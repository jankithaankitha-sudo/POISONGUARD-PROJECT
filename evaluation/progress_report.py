
import os
import pandas as pd

RESULTS_DIR = "reports/results"


def main():
    detection_path = os.path.join(
        RESULTS_DIR, "detection_experiment_results.csv"
    )

    mitigation_path = os.path.join(
        RESULTS_DIR, "week6_mitigation_results.csv"
    )

    output_path = os.path.join(
        RESULTS_DIR, "progress_summary.txt"
    )

    os.makedirs(RESULTS_DIR, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as report:
        report.write("POISONGUARD - PROJECT PROGRESS REPORT\n")
        report.write("=" * 45 + "\n\n")

        # Detection evaluation results
        report.write("1. DETECTION EVALUATION RESULTS\n")
        report.write("-" * 35 + "\n")

        if os.path.exists(detection_path):
            detection_data = pd.read_csv(detection_path)
            report.write(
                detection_data.to_string(index=False)
            )
            report.write("\n\n")
        else:
            report.write(
                "Detection results file not found.\n\n"
            )

        # Mitigation evaluation results
        report.write("2. MITIGATION EVALUATION RESULTS\n")
        report.write("-" * 35 + "\n")

        if os.path.exists(mitigation_path):
            mitigation_data = pd.read_csv(mitigation_path)
            report.write(
                mitigation_data.to_string(index=False)
            )
            report.write("\n\n")
        else:
            report.write(
                "Mitigation results file not found.\n\n"
            )

        # Limitations
        report.write("3. LIMITATIONS\n")
        report.write("-" * 35 + "\n")
        report.write(
            "Anomaly detection may flag clean samples as suspicious "
            "and may miss poisoned samples. Results should be "
            "interpreted using the known simulated poison labels.\n\n"
        )

        report.write("4. CONCLUSION\n")
        report.write("-" * 35 + "\n")
        report.write(
            "The experiments compare detection methods and model "
            "performance before and after mitigation. Further "
            "improvements are needed to reduce false positives "
            "and false negatives.\n"
        )

    print("Progress report generated successfully!")
    print("Saved to:", output_path)


if __name__ == "__main__":
    main()
