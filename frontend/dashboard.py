import streamlit as st
import requests


BACKEND_URL = "http://127.0.0.1:5000"


st.set_page_config(
    page_title="PoisonGuard",
    page_icon="🛡️",
    layout="wide"
)


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

    


st.sidebar.header("PoisonGuard Pipeline")


if st.sidebar.button(
    "1️⃣ Train Baseline"
):

    result = call_api(
        "/api/baseline"
    )

    if result:

        st.session_state["baseline"] = result

        st.success(
            "Baseline model trained successfully."
        )


if st.sidebar.button(
    "2️⃣ Run Poisoning Attack"
):

    result = call_api(
        "/api/poisoning"
    )

    if result:

        st.session_state["poisoning"] = result

        st.warning(
            "Label-flip poisoning attack executed."
        )


if st.sidebar.button(
    "3️⃣ Detect Poison"
):

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


if st.sidebar.button(
    "4️⃣ Run Backdoor Attack"
):

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


if st.sidebar.button(
    "5️⃣ Detect Backdoor"
):

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


if st.sidebar.button(
    "6️⃣ Mitigate & Retrain"
):

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


if st.sidebar.button(
    "7️⃣ Final Evaluation"
):

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


st.divider()


st.header("📊 PoisonGuard Dashboard")


col1, col2, col3, col4 = st.columns(4)


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


with col1:

    st.metric(
        "Baseline Accuracy",
        baseline["results"]["accuracy"]
        if baseline else "—"
    )


with col2:

    st.metric(
        "Poisoned Samples",
        poisoning["poisoned_samples"]
        if poisoning else "—"
    )


with col3:

    st.metric(
        "Detected Samples",
        poison_detection["suspicious_count"]
        if poison_detection else "—"
    )


with col4:

    st.metric(
        "Final Accuracy",
        mitigation[
            "final_results"
        ]["accuracy"]
        if mitigation
        else "—"
    )


st.divider()


st.header("🔬 Detection Results")


if "poison_detection" in st.session_state:

    st.subheader(
        "Data Poisoning Detection"
    )

    st.json(
        st.session_state[
            "poison_detection"
        ]
    )


if "backdoor_detection" in st.session_state:

    st.subheader(
        "Backdoor Detection"
    )

    st.json(
        st.session_state[
            "backdoor_detection"
        ]
    )


st.header("📈 Model Evaluation")


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


st.divider()


st.header("🔐 Model Integrity")


if st.button(
    "Check Final Model Integrity"
):

    try:

        response = requests.get(
            BACKEND_URL
            + "/api/model-integrity"
        )

        result = response.json()

        st.json(result)

    except Exception as error:

        st.error(str(error))


st.divider()


st.caption(
    "PoisonGuard | ML Security & Supply Chain Defense"
)