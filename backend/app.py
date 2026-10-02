from flask import Flask, jsonify

import hashlib
import os

from models.model_engine import (
    load_dataset,
    split_dataset,
    train_model,
    evaluate_model,
    save_model
)

from attacks.poisoning.label_flip import (
    label_flip_attack
)

from attacks.backdoor.feature_trigger import (
    backdoor_attack
)

from detection.poison_detection import (
    detect_poisoned_samples
)

from detection.backdoor_detection import (
    detect_backdoor
)

from mitigation.mitigation import (
    remove_suspicious_samples
)


app = Flask(__name__)


PROJECT_STATE = {}


def calculate_file_hash(filepath):

    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:

        for chunk in iter(
            lambda: file.read(4096),
            b""
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


@app.route("/")
def home():

    return jsonify({
        "project": "PoisonGuard",
        "status": "running",
        "description":
            "ML Data Poisoning and Backdoor Defense Framework"
    })


@app.route("/api/health")
def health():

    return jsonify({
        "status": "healthy",
        "backend": "Flask",
        "ml_engine": "Random Forest"
    })


@app.route("/api/baseline", methods=["POST"])
def baseline():

    X, y = load_dataset()

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = split_dataset(X, y)

    model = train_model(
        X_train,
        y_train
    )

    results = evaluate_model(
        model,
        X_test,
        y_test
    )

    model_path = save_model(
        model,
        "baseline_model.pkl"
    )

    PROJECT_STATE["X_train"] = X_train
    PROJECT_STATE["X_test"] = X_test
    PROJECT_STATE["y_train"] = y_train
    PROJECT_STATE["y_test"] = y_test
    PROJECT_STATE["baseline_model"] = model

    return jsonify({
        "stage": "baseline",
        "model": "Random Forest",
        "results": results,
        "model_path": model_path
    })


@app.route("/api/poisoning", methods=["POST"])
def poisoning():

    X_train = PROJECT_STATE["X_train"]
    y_train = PROJECT_STATE["y_train"]

    (
        X_poisoned,
        y_poisoned,
        indices
    ) = label_flip_attack(
        X_train,
        y_train,
        poison_rate=0.10
    )

    poisoned_model = train_model(
        X_poisoned,
        y_poisoned
    )

    results = evaluate_model(
        poisoned_model,
        PROJECT_STATE["X_test"],
        PROJECT_STATE["y_test"]
    )

    PROJECT_STATE["X_poisoned"] = X_poisoned
    PROJECT_STATE["y_poisoned"] = y_poisoned
    PROJECT_STATE["poisoned_model"] = poisoned_model
    PROJECT_STATE["poison_indices"] = indices

    save_model(
        poisoned_model,
        "poisoned_model.pkl"
    )

    return jsonify({
        "stage": "label_flip_poisoning",
        "poison_rate": 0.10,
        "poisoned_samples": int(len(indices)),
        "results": results
    })


@app.route("/api/poison-detection", methods=["POST"])
def poison_detection():

    result = detect_poisoned_samples(
        PROJECT_STATE["poisoned_model"],
        PROJECT_STATE["X_poisoned"],
        PROJECT_STATE["y_poisoned"]
    )

    PROJECT_STATE["poison_detection"] = result

    return jsonify(result)


@app.route("/api/backdoor", methods=["POST"])
def backdoor():

    X_train = PROJECT_STATE["X_train"]
    y_train = PROJECT_STATE["y_train"]

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
        target_label=1
    )

    backdoor_model = train_model(
        X_backdoor,
        y_backdoor
    )

    results = evaluate_model(
        backdoor_model,
        PROJECT_STATE["X_test"],
        PROJECT_STATE["y_test"]
    )

    PROJECT_STATE["X_backdoor"] = X_backdoor
    PROJECT_STATE["y_backdoor"] = y_backdoor
    PROJECT_STATE["backdoor_model"] = backdoor_model
    PROJECT_STATE["backdoor_indices"] = indices
    PROJECT_STATE["trigger_feature"] = trigger_feature
    PROJECT_STATE["trigger_value"] = trigger_value

    save_model(
        backdoor_model,
        "backdoor_model.pkl"
    )

    return jsonify({
        "stage": "backdoor_attack",
        "poison_rate": 0.05,
        "poisoned_samples": int(len(indices)),
        "trigger_feature": int(trigger_feature),
        "trigger_value": float(trigger_value),
        "results": results
    })


@app.route("/api/backdoor-detection", methods=["POST"])
def backdoor_detection():

    result = detect_backdoor(
        PROJECT_STATE["backdoor_model"],
        PROJECT_STATE["X_test"],
        PROJECT_STATE["trigger_feature"],
        PROJECT_STATE["trigger_value"]
    )

    PROJECT_STATE["backdoor_detection"] = result

    return jsonify(result)


@app.route("/api/mitigate", methods=["POST"])
def mitigate():

    if "poison_detection" not in PROJECT_STATE:

        return jsonify({
            "error":
                "Run poison detection first."
        }), 400

    X_poisoned = PROJECT_STATE["X_poisoned"]
    y_poisoned = PROJECT_STATE["y_poisoned"]

    suspicious_indices = PROJECT_STATE[
        "poison_detection"
    ]["suspicious_indices"]

    X_clean, y_clean = (
        remove_suspicious_samples(
            X_poisoned,
            y_poisoned,
            suspicious_indices
        )
    )

    final_model = train_model(
        X_clean,
        y_clean
    )

    results = evaluate_model(
        final_model,
        PROJECT_STATE["X_test"],
        PROJECT_STATE["y_test"]
    )

    final_path = save_model(
        final_model,
        "final_model.pkl"
    )

    PROJECT_STATE["final_model"] = final_model

    return jsonify({
        "stage": "mitigation",
        "removed_samples": len(
            suspicious_indices
        ),
        "remaining_samples": len(y_clean),
        "final_results": results,
        "final_model": final_path
    })


@app.route("/api/evaluation", methods=["POST"])
def evaluation():

    result = {}

    if "baseline_model" in PROJECT_STATE:

        result["baseline"] = evaluate_model(
            PROJECT_STATE["baseline_model"],
            PROJECT_STATE["X_test"],
            PROJECT_STATE["y_test"]
        )

    if "poisoned_model" in PROJECT_STATE:

        result["poisoned"] = evaluate_model(
            PROJECT_STATE["poisoned_model"],
            PROJECT_STATE["X_test"],
            PROJECT_STATE["y_test"]
        )

    if "final_model" in PROJECT_STATE:

        result["final"] = evaluate_model(
            PROJECT_STATE["final_model"],
            PROJECT_STATE["X_test"],
            PROJECT_STATE["y_test"]
        )

    return jsonify(result)


@app.route("/api/model-integrity")
def model_integrity():

    path = "models/trained_models/final_model.pkl"

    if not os.path.exists(path):

        return jsonify({
            "status": "not_available"
        })

    file_hash = calculate_file_hash(path)

    return jsonify({
        "status": "verified",
        "algorithm": "SHA-256",
        "hash": file_hash
    })


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )