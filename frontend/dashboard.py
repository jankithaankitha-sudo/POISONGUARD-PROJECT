import streamlit as st
import requests
import pandas as pd
import os


# ==========================================
# CONFIGURATION
# ==========================================

BACKEND_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="PoisonGuard",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("🛡️ PoisonGuard")

st.subheader(
    "Automated Framework for Detecting and Preventing "
    "Data Poisoning and Backdoor Attacks"
)

st.markdown(
    """
    **Cybersecurity & Machine Learning Security**

    PoisonGuard demonstrates:

    - Data poisoning attacks
    - Backdoor attacks
    - Poison detection
    - Backdoor detection
    - Mitigation
    - Model retraining
    - Evaluation
    - Model integrity verification
    """
)


# ==========================================
# API FUNCTION - POST
# ==========================================

def call_api(endpoint):
    try:
        response = requests.post(
            BACKEND_URL + endpoint,
            timeout=120
        )

        if response.status_code != 200:
            st.error(
                f"Backend returned HTTP {response.status_code}"
            )
            st.code(response.text)
            return None

        try:
            return response.json()

        except ValueError:
            st.error(
                "Backend returned a non-JSON response."
            )
            st.code(response.text)
            return None

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to Flask backend. "
            "Make sure Flask is running on port 5000."
        )
        return None

    except requests.exceptions.Timeout:
        st.error(
            "Backend request timed out."
        )
        return None

    except Exception as error:
        st.error(
            f"Unexpected error: {error}"
        )
        return None


# ==========================================
# API FUNCTION - GET
# ==========================================

def call_get_api(endpoint):
    try:
        response = requests.get(
            BACKEND_URL + endpoint,
            timeout=120
        )

        if response.status_code != 200:
            st.error(
                f"Backend returned HTTP {response.status_code}"
            )
            st.code(response.text)
            return None

        try:
            return response.json()

        except ValueError:
            st.error(
                "Backend returned a non-JSON response."
            )
            st.code(response.text)
            return None

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to Flask backend. "
            "Make sure Flask is running on port 5000."
        )
        return None

    except requests.exceptions.Timeout:
        st.error(
            "Backend request timed out."
        )
        return None

    except Exception as error:
        st.error(
            f"Unexpected error: {error}"
        )
        return None


# ==========================================
# SIDEBAR PIPELINE
# ==========================================

st.sidebar.header("PoisonGuard Pipeline")


# ==========================================
# 1. TRAIN BASELINE
# ==========================================

if st.sidebar.button("1️⃣ Train Baseline"):

    result = call_api("/api/baseline")

    if result:

        st.session_state["baseline"] = result

        st.success(
            "Baseline model trained successfully."
        )


# ==========================================
# 2. RUN POISONING ATTACK
# ==========================================

if st.sidebar.button("2️⃣ Run Poisoning Attack"):

    result = call_api("/api/poisoning")

    if result:

        st.session_state["poisoning"] = result

        st.warning(
            "Label-flip poisoning attack executed."
        )


# ==========================================
# 3. DETECT POISON
# ==========================================

if st.sidebar.button("3️⃣ Detect Poison"):

    result = call_api(
        "/api/poison-detection"
    )

    if result:

        st.session_state[
            "poison_detection"
        ] = result

        st.info(
            "Poison detection completed."
        )


# ==========================================
# 4. RUN BACKDOOR ATTACK
# ==========================================

if st.sidebar.button("4️⃣ Run Backdoor Attack"):

    result = call_api(
        "/api/backdoor"
    )

    if result:

        st.session_state[
            "backdoor"
        ] = result

        st.warning(
            "Backdoor attack executed."
        )


# ==========================================
# 5. DETECT BACKDOOR
# ==========================================

if st.sidebar.button("5️⃣ Detect Backdoor"):

    result = call_api(
        "/api/backdoor-detection"
    )

    if result:

        st.session_state[
            "backdoor_detection"
        ] = result

        st.info(
            "Backdoor detection completed."
        )


# ==========================================
# 6. MITIGATE AND RETRAIN
# ==========================================

if st.sidebar.button("6️⃣ Mitigate & Retrain"):

    result = call_api(
        "/api/mitigate"
    )

    if result:

        st.session_state[
            "mitigation"
        ] = result

        st.success(
            "Mitigation and retraining completed."
        )


# ==========================================
# 7. FINAL EVALUATION
# ==========================================

if st.sidebar.button("7️⃣ Final Evaluation"):

    result = call_api(
        "/api/evaluation"
    )

    if result:

        st.session_state[
            "evaluation"
        ] = result

        st.success(
            "Evaluation completed."
        )


# ==========================================
# 8. MODEL INTEGRITY
# ==========================================

if st.sidebar.button(
    "8️⃣ Check Final Model Integrity"
):

    result = call_get_api(
        "/api/model-integrity"
    )

    if result:

        st.session_state[
            "integrity"
        ] = result

        st.success(
            "Model integrity verification completed."
        )


# ==========================================
# MAIN DASHBOARD
# ==========================================

st.divider()

st.header(
    "📊 PoisonGuard Dashboard"
)


# ==========================================
# GET SESSION STATE
# ==========================================

baseline = st.session_state.get(
    "baseline"
)

poisoning = st.session_state.get(
    "poisoning"
)

poison_detection = st.session_state.get(
    "poison_detection"
)

mitigation = st.session_state.get(
    "mitigation"
)


# ==========================================
# DASHBOARD CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)


# ==========================================
# BASELINE ACCURACY
# ==========================================

with col1:

    if baseline and "results" in baseline:

        baseline_accuracy = baseline[
            "results"
        ].get(
            "accuracy",
            "—"
        )

    else:

        baseline_accuracy = "—"

    st.metric(
        "Baseline Accuracy",
        baseline_accuracy
    )


# ==========================================
# POISONED SAMPLES
# ==========================================

with col2:

    if poisoning:

        poisoned_samples = poisoning.get(
            "poisoned_samples"
        )

        if poisoned_samples is None:

            poisoned_samples = poisoning.get(
                "actual_poisoned"
            )

        if poisoned_samples is None:

            poisoned_samples = "—"

    else:

        poisoned_samples = "—"

    st.metric(
        "Poisoned Samples",
        poisoned_samples
    )


# ==========================================
# DETECTED SAMPLES
# ==========================================

with col3:

    if poison_detection:

        detected_samples = poison_detection.get(
            "suspicious_count",
            "—"
        )

    else:

        detected_samples = "—"

    st.metric(
        "Detected Samples",
        detected_samples
    )


# ==========================================
# FINAL ACCURACY
# ==========================================

with col4:

    final_accuracy = "—"

    if mitigation:

        if "final_results" in mitigation:

            final_accuracy = mitigation[
                "final_results"
            ].get(
                "accuracy",
                "—"
            )

        elif "accuracy" in mitigation:

            final_accuracy = mitigation[
                "accuracy"
            ]

    st.metric(
        "Final Accuracy",
        final_accuracy
    )


# ==========================================
# POISONING RATE EXPERIMENTS
# ==========================================

st.divider()

st.header(
    "🧪 Poisoning Rate Experiments"
)


experiment_file = (
    "reports/results/"
    "poisoning_experiment_results.csv"
)


if os.path.exists(experiment_file):

    try:

        experiment_data = pd.read_csv(
            experiment_file
        )


        # ======================================
        # RESULTS TABLE
        # ======================================

        st.subheader(
            "Performance at Different Poisoning Rates"
        )

        st.dataframe(
            experiment_data,
            use_container_width=True
        )


        # ======================================
        # ACCURACY GRAPH
        # ======================================

        st.subheader(
            "📈 Accuracy vs Poisoning Rate"
        )

        chart_data = experiment_data[
            [
                "poisoning_rate",
                "accuracy"
            ]
        ].copy()

        chart_data[
            "poisoning_rate"
        ] = pd.to_numeric(
            chart_data[
                "poisoning_rate"
            ]
        )

        chart_data = chart_data.sort_values(
            "poisoning_rate"
        )

        chart_data = chart_data.reset_index(
            drop=True
        )

        st.line_chart(
            chart_data,
            x="poisoning_rate",
            y="accuracy"
        )


        # ======================================
        # PRECISION RECALL F1 GRAPH
        # ======================================

        st.subheader(
            "📊 Precision, Recall and F1 Score"
        )

        metrics_data = experiment_data[
            [
                "poisoning_rate",
                "precision",
                "recall",
                "f1_score"
            ]
        ].copy()

        metrics_data[
            "poisoning_rate"
        ] = pd.to_numeric(
            metrics_data[
                "poisoning_rate"
            ]
        )

        metrics_data = metrics_data.sort_values(
            "poisoning_rate"
        )

        metrics_data = metrics_data.reset_index(
            drop=True
        )

        st.line_chart(
            metrics_data,
            x="poisoning_rate",
            y=[
                "precision",
                "recall",
                "f1_score"
            ]
        )


    except Exception as error:

        st.error(
            f"Could not load experiment results: {error}"
        )


else:

    st.info(
        "Poisoning experiment results file not found."
    )


# ==========================================
# DETECTION RESULTS
# ==========================================

st.divider()

st.header(
    "🔬 Detection Results"
)


# ==========================================
# DATA POISONING DETECTION
# ==========================================

if "poison_detection" in st.session_state:

    st.subheader(
        "Data Poisoning Detection"
    )

    st.json(
        st.session_state[
            "poison_detection"
        ]
    )


# ==========================================
# BACKDOOR DETECTION
# ==========================================

if "backdoor_detection" in st.session_state:

    st.subheader(
        "Backdoor Detection"
    )

    st.json(
        st.session_state[
            "backdoor_detection"
        ]
    )


# ==========================================
# MODEL EVALUATION
# ==========================================

st.divider()

st.header(
    "📈 Model Evaluation"
)


if "evaluation" in st.session_state:

    evaluation = st.session_state[
        "evaluation"
    ]

    for model_name, result in evaluation.items():

        st.subheader(
            model_name.title()
        )

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Accuracy",
                result["accuracy"]
            )


        with col2:

            st.metric(
                "Precision",
                result["precision"]
            )


        with col3:

            st.metric(
                "Recall",
                result["recall"]
            )


        with col4:

            st.metric(
                "F1",
                result["f1_score"]
            )


# ==========================================
# MODEL INTEGRITY
# ==========================================

st.divider()

st.header(
    "🔐 Model Integrity"
)


if "integrity" in st.session_state:

    st.json(
        st.session_state[
            "integrity"
        ]
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "PoisonGuard | ML Security & Supply Chain Defense"
)
