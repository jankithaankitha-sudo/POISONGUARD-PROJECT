from models.model_engine import evaluate_model


def compare_models(
    baseline_model,
    poisoned_model,
    final_model,
    X_test,
    y_test
):

    baseline_results = evaluate_model(
        baseline_model,
        X_test,
        y_test
    )

    poisoned_results = evaluate_model(
        poisoned_model,
        X_test,
        y_test
    )

    final_results = evaluate_model(
        final_model,
        X_test,
        y_test
    )

    return {
        "baseline": baseline_results,
        "poisoned": poisoned_results,
        "final": final_results
    }