import os
import time

import requests
import streamlit as st


st.set_page_config(
    page_title="Loan Prediction App",
    page_icon=":bar_chart:",
    layout="wide",
)


AUTHOR_NAME = "Nipun"
GITHUB_URL = "https://github.com/Nipun1a"
LINKEDIN_URL = "https://www.linkedin.com/in/nipun-pal-450805294/"
CONTACT_EMAIL = "nipun7abc@gmail.com"
DEFAULT_BACKEND_BASE_URL = "http://127.0.0.1:8000"
MIN_LOADER_SECONDS = 2.5


def get_api_url() -> str:
    secret_backend_url = st.secrets.get("BACKEND_URL") if hasattr(st, "secrets") else None
    env_backend_url = os.getenv("BACKEND_URL")
    backend_base_url = (secret_backend_url or env_backend_url or DEFAULT_BACKEND_BASE_URL).rstrip("/")
    return f"{backend_base_url}/predict"


API_URL = get_api_url()


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

        :root {
            --bg-main: #0b1220;
            --bg-panel: rgba(10, 18, 32, 0.82);
            --bg-field: rgba(148, 163, 184, 0.12);
            --border: rgba(148, 163, 184, 0.18);
            --text-main: #f8fafc;
            --text-soft: #cbd5e1;
            --accent: #22c55e;
            --accent-2: #0ea5e9;
            --danger: #f97316;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(14, 165, 233, 0.22), transparent 32%),
                radial-gradient(circle at top right, rgba(34, 197, 94, 0.18), transparent 28%),
                linear-gradient(180deg, #020617 0%, #0b1220 45%, #111827 100%);
            color: var(--text-main);
            font-family: 'Space Grotesk', sans-serif;
        }

        .block-container {
            max-width: 1120px;
            padding-top: 2.5rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3, label, p, div, span {
            font-family: 'Space Grotesk', sans-serif !important;
        }

        .hero-card,
        .form-card,
        .footer-card {
            background: var(--bg-panel);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            border-radius: 24px;
            box-shadow: 0 24px 70px rgba(2, 6, 23, 0.35);
        }

        .hero-card {
            padding: 2rem;
            margin-bottom: 1.25rem;
        }

        .hero-kicker {
            display: inline-block;
            margin-bottom: 0.8rem;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: rgba(14, 165, 233, 0.12);
            color: #7dd3fc;
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .hero-title {
            margin: 0;
            font-size: clamp(2.5rem, 5vw, 4.6rem);
            line-height: 0.95;
            letter-spacing: -0.04em;
        }

        .hero-copy {
            margin: 1rem 0 0;
            max-width: 700px;
            color: var(--text-soft);
            font-size: 1.05rem;
            line-height: 1.7;
        }

        .form-card {
            padding: 1.4rem 1.4rem 1.1rem;
            margin-bottom: 1rem;
        }

        .section-title {
            margin: 0 0 1rem;
            color: var(--text-main);
            font-size: 1rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }

        div[data-baseweb="input"],
        div[data-baseweb="select"] > div {
            background: var(--bg-field) !important;
            border: 1px solid transparent !important;
            border-radius: 18px !important;
            min-height: 58px;
        }

        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="select"] > div:focus-within {
            border-color: rgba(34, 197, 94, 0.55) !important;
            box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.14);
        }

        .stNumberInput input,
        .stSelectbox label,
        .stNumberInput label {
            color: var(--text-main) !important;
        }

        .stNumberInput input {
            font-size: 1.02rem !important;
            font-weight: 500 !important;
        }

        .stButton > button {
            width: 100%;
            min-height: 62px;
            margin-top: 0.75rem;
            border: none;
            border-radius: 18px;
            background: linear-gradient(135deg, var(--accent-2), var(--accent));
            color: white;
            font-size: 1.05rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            box-shadow: 0 22px 45px rgba(14, 165, 233, 0.28);
            transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            filter: brightness(1.03);
            box-shadow: 0 28px 60px rgba(34, 197, 94, 0.22);
        }

        .stAlert {
            border-radius: 18px;
            border-width: 1px;
        }

        .result-card {
            margin-top: 1rem;
            padding: 1.5rem 1.6rem;
            border-radius: 24px;
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 24px 60px rgba(2, 6, 23, 0.28);
        }

        .result-card--high {
            background: linear-gradient(135deg, rgba(127, 29, 29, 0.68), rgba(153, 27, 27, 0.42));
            border-color: rgba(248, 113, 113, 0.28);
        }

        .result-card--low {
            background: linear-gradient(135deg, rgba(20, 83, 45, 0.74), rgba(21, 128, 61, 0.38));
            border-color: rgba(74, 222, 128, 0.26);
        }

        .result-label {
            margin: 0 0 0.45rem;
            font-size: 0.92rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: rgba(248, 250, 252, 0.78);
        }

        .result-title {
            margin: 0;
            font-size: clamp(1.5rem, 2.4vw, 2.2rem);
            line-height: 1.15;
            font-weight: 700;
            color: #f8fafc;
        }

        .result-probability {
            margin-top: 0.9rem;
            font-size: clamp(2rem, 4.4vw, 3.2rem);
            line-height: 1;
            font-weight: 700;
            color: #f8fafc;
        }

        .result-copy {
            margin: 0.75rem 0 0;
            color: rgba(248, 250, 252, 0.84);
            font-size: 1rem;
            line-height: 1.6;
        }

        .footer-card {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            margin-top: 1.2rem;
            padding: 1.15rem 1.4rem;
            align-items: center;
            flex-wrap: wrap;
        }

        .footer-credit {
            color: var(--text-soft);
            font-size: 0.98rem;
        }

        .footer-links {
            display: flex;
            gap: 0.9rem;
            flex-wrap: wrap;
        }

        .footer-links a {
            color: var(--text-main);
            text-decoration: none;
            padding: 0.55rem 0.9rem;
            border-radius: 999px;
            background: rgba(148, 163, 184, 0.12);
            border: 1px solid rgba(148, 163, 184, 0.18);
            transition: background 0.18s ease, transform 0.18s ease;
        }

        .footer-links a:hover {
            background: rgba(14, 165, 233, 0.18);
            transform: translateY(-1px);
        }

        @media (max-width: 768px) {
            .block-container {
                padding-top: 1.25rem;
            }

            .hero-card,
            .form-card,
            .footer-card {
                border-radius: 20px;
            }

            .hero-card {
                padding: 1.35rem;
            }

            .form-card {
                padding: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if API_URL.startswith(DEFAULT_BACKEND_BASE_URL):
    st.info(
        "Using the local backend URL. For Streamlit Cloud, set `BACKEND_URL` in Secrets "
        "to your Render backend URL."
    )


st.markdown(
    """
    <div class="hero-card">
        <div class="hero-kicker">Smart Risk Screening</div>
        <h1 class="hero-title">Loan Prediction App</h1>
        <p class="hero-copy">
            Enter the applicant profile below to estimate loan risk with a cleaner workflow,
            safer input controls, and a clearer prediction summary.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


with st.form("loan_prediction_form"):
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Applicant Details</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1, format="%d")
        income = st.number_input("Income", min_value=0, value=50000, step=1000, format="%d")
        emp_exp = st.number_input(
            "Employment Experience",
            min_value=0,
            max_value=80,
            value=5,
            step=1,
            format="%d",
        )
        loan_amnt = st.number_input("Loan Amount", min_value=0, value=10000, step=500, format="%d")
        loan_int_rate = st.number_input(
            "Interest Rate",
            min_value=0.0,
            max_value=100.0,
            value=12.5,
            step=0.1,
            format="%.2f",
        )

    with col2:
        loan_percent_income = st.number_input(
            "Loan % Income",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=0.1,
            format="%.2f",
        )
        cred_hist = st.number_input(
            "Credit History Length",
            min_value=0,
            max_value=80,
            value=6,
            step=1,
            format="%d",
        )
        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=850,
            value=680,
            step=1,
            format="%d",
        )
        gender = st.selectbox("Gender", ["male", "female"])
        education = st.selectbox(
            "Education",
            ["High School", "Associate", "Bachelor", "Master", "Doctorate"],
        )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Loan Profile</p>', unsafe_allow_html=True)
    col3, col4, col5 = st.columns(3, gap="large")

    with col3:
        home = st.selectbox("Home Ownership", ["RENT", "OWN", "MORTGAGE", "OTHER"])

    with col4:
        intent = st.selectbox(
            "Loan Intent",
            ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"],
        )

    with col5:
        default = st.selectbox("Previous Default", ["Yes", "No"])

    submit = st.form_submit_button("Predict Loan Risk")
    st.markdown('</div>', unsafe_allow_html=True)


if submit:
    data = {
        "person_age": int(age),
        "person_gender": gender,
        "person_education": education,
        "person_income": int(income),
        "person_emp_exp": int(emp_exp),
        "person_home_ownership": home,
        "loan_amnt": int(loan_amnt),
        "loan_intent": intent,
        "loan_int_rate": float(loan_int_rate),
        "loan_percent_income": float(loan_percent_income),
        "cb_person_cred_hist_length": int(cred_hist),
        "credit_score": int(credit_score),
        "previous_loan_defaults_on_file": default,
    }

    with st.spinner("Analyzing profile and preparing prediction..."):
        start_time = time.perf_counter()
        try:
            response = requests.post(API_URL, json=data, timeout=15)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as exc:
            st.error(f"Could not connect to the prediction API. Details: {exc}")
            result = None
        elapsed = time.perf_counter() - start_time
        if elapsed < MIN_LOADER_SECONDS:
            time.sleep(MIN_LOADER_SECONDS - elapsed)

    if result:
        if "prediction" in result:
            probability = float(result.get("probability", 0.0))
            risk_percent = probability * 100

            if result["prediction"] == 1:
                st.markdown(
                    f"""
                    <div class="result-card result-card--high">
                        <p class="result-label">Prediction Result</p>
                        <p class="result-title">High Risk Applicant</p>
                        <div class="result-probability">{risk_percent:.1f}%</div>
                        <p class="result-copy">
                            Estimated default probability based on the entered applicant profile.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="result-card result-card--low">
                        <p class="result-label">Prediction Result</p>
                        <p class="result-title">Low Risk Applicant</p>
                        <div class="result-probability">{risk_percent:.1f}%</div>
                        <p class="result-copy">
                            Estimated default probability based on the entered applicant profile.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.warning(result.get("error", "Prediction could not be generated."))


st.markdown(
    f"""
    <div class="footer-card">
        <div class="footer-credit">Made by {AUTHOR_NAME}</div>
        <div class="footer-links">
            <a href="{LINKEDIN_URL}" target="_blank">LinkedIn</a>
            <a href="{GITHUB_URL}" target="_blank">GitHub</a>
            <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
