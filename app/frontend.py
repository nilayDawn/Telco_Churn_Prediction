import os
import textwrap

import requests
import streamlit as st
import streamlit.components.v1 as components

from src.models.explainability import ModelExplainer

API_URL = os.getenv("API_URL", "http://localhost:8000")

@st.cache_resource
def load_explainer():
    return ModelExplainer()

explainer = load_explainer()

st.set_page_config(
    page_title="ChurnAI | Customer Churn Predictor",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    textwrap.dedent("""
    <style>
    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(99, 102, 241, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(139, 92, 246, 0.10),
                transparent 30%
            ),
            #0b0f19;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    .hero {
        padding: 35px 40px;
        border-radius: 24px;
        margin-bottom: 30px;
        background:
            linear-gradient(
                135deg,
                rgba(79, 70, 229, 0.25),
                rgba(124, 58, 237, 0.18),
                rgba(15, 23, 42, 0.8)
            );
        border: 1px solid rgba(148, 163, 184, 0.15);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(
            90deg,
            #ffffff,
            #a5b4fc,
            #c4b5fd
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 17px;
        color: #94a3b8;
        margin-top: 10px;
        max-width: 750px;
    }

    .status-badge {
        display: inline-block;
        margin-top: 18px;
        padding: 7px 14px;
        border-radius: 999px;
        background: rgba(34, 197, 94, 0.12);
        border: 1px solid rgba(34, 197, 94, 0.25);
        color: #86efac;
        font-size: 13px;
        font-weight: 600;
    }

    .section-card {
        padding: 22px 24px;
        border-radius: 18px;
        margin-bottom: 12px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.12);
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.18);
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 3px;
    }

    .section-description {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 15px;
    }

    label {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        border-color: #334155 !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="input"] {
        background-color: #111827 !important;
        border-radius: 10px !important;
    }

    input {
        color: #f8fafc !important;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        border: none !important;
        border-radius: 12px !important;
        background:
            linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            ) !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        padding: 14px 25px !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.30);
        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.45);
    }

    .result-card {
        padding: 30px;
        border-radius: 22px;
        margin-top: 20px;
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.95),
                rgba(30, 41, 59, 0.75)
            );
        border: 1px solid rgba(148, 163, 184, 0.16);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.30);
    }

    .result-label {
        color: #94a3b8;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .probability {
        font-size: 58px;
        font-weight: 800;
        margin-top: 5px;
        background: linear-gradient(
            90deg,
            #818cf8,
            #c4b5fd
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .risk-badge {
        display: inline-block;
        padding: 8px 18px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 14px;
        margin-top: 8px;
    }

    .risk-high {
        background: rgba(239, 68, 68, 0.12);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.25);
    }

    .risk-medium {
        background: rgba(245, 158, 11, 0.12);
        color: #fcd34d;
        border: 1px solid rgba(245, 158, 11, 0.25);
    }

    .risk-low {
        background: rgba(34, 197, 94, 0.12);
        color: #86efac;
        border: 1px solid rgba(34, 197, 94, 0.25);
    }

    .metric-card {
        padding: 18px;
        border-radius: 16px;
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(148, 163, 184, 0.12);
        text-align: center;
    }

    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #f8fafc;
    }

    .metric-label {
        font-size: 12px;
        color: #64748b;
        margin-top: 4px;
    }

    .footer {
        text-align: center;
        margin-top: 45px;
        color: #475569;
        font-size: 12px;
    }

    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
    </style>
    """),
    unsafe_allow_html=True,
)

st.markdown(
    textwrap.dedent("""
    <div class="hero">
        <div class="hero-title">🔮 ChurnAI</div>
        <div class="hero-subtitle">
            AI-powered customer churn prediction platform.
            Analyze customer behavior, subscription services and
            billing information to identify customers at risk of leaving.
        </div>
        <div class="status-badge">● AI Prediction Engine Online</div>
    </div>
    """),
    unsafe_allow_html=True,
)

with st.form("churn_form"):
    st.markdown(
        textwrap.dedent("""
        <div class="section-card">
            <div class="section-title">👤 Customer Profile</div>
            <div class="section-description">Basic demographic and customer relationship information</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        gender = st.selectbox("Gender", ["Female", "Male"])

    with col2:
        senior = st.selectbox("Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

    with col3:
        partner = st.selectbox("Partner", ["Yes", "No"])

    with col4:
        dependents = st.selectbox("Dependents", ["Yes", "No"])

    with col5:
        tenure = st.number_input("Tenure (Months)", min_value=0, max_value=120, value=12)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        textwrap.dedent("""
        <div class="section-card">
            <div class="section-title">📡 Services & Subscriptions</div>
            <div class="section-description">Customer's active telecommunications and streaming services</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        phone = st.selectbox("Phone Service", ["Yes", "No"])
        multiple = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
        internet = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])

    with col2:
        security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
        device = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])

    with col3:
        tech = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
        movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        textwrap.dedent("""
        <div class="section-card">
            <div class="section-title">💳 Account & Billing</div>
            <div class="section-description">Contract, payment and customer spending information</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

    with col2:
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])

    with col3:
        payment = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ],
        )

    with col4:
        monthly = st.number_input("Monthly Charges ($)", min_value=0.0, value=70.35, step=0.5)

    with col5:
        total = st.number_input("Total Charges ($)", min_value=0.0, value=844.20, step=1.0)

    st.markdown("<br>", unsafe_allow_html=True)

    submit_button = st.form_submit_button("🚀  Analyze Customer & Predict Churn", use_container_width=True)

if submit_button:
    payload = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": int(tenure),
        "PhoneService": phone,
        "MultipleLines": multiple,
        "InternetService": internet,
        "OnlineSecurity": security,
        "OnlineBackup": backup,
        "DeviceProtection": device,
        "TechSupport": tech,
        "StreamingTV": tv,
        "StreamingMovies": movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": float(monthly),
        "TotalCharges": float(total),
    }

    try:
        with st.spinner("🤖 AI is analyzing the customer profile..."):
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()
            prob = result["churn_probability"] * 100
            risk = result["risk_level"]
            prediction = result["churn_prediction"]

            risk_lower = str(risk).lower()
            if "high" in risk_lower:
                risk_class = "risk-high"
                risk_icon = "🔴"
                result_title = "High Churn Risk"
            elif "medium" in risk_lower:
                risk_class = "risk-medium"
                risk_icon = "🟡"
                result_title = "Moderate Churn Risk"
            else:
                risk_class = "risk-low"
                risk_icon = "🟢"
                result_title = "Low Churn Risk"

            st.markdown(
                textwrap.dedent("""
                <br>
                <div class="result-card">
                    <div class="result-label">AI PREDICTION RESULT</div>
                </div>
                """),
                unsafe_allow_html=True,
            )

            result_col1, result_col2 = st.columns([1.3, 1], gap="large")

            with result_col1:
                st.markdown(
                    textwrap.dedent(f"""
                    <div class="result-card">
                        <div style="font-size:18px; color:#94a3b8;">Prediction</div>
                        <div style="font-size:32px; font-weight:800; margin-top:8px;">
                            {risk_icon} {result_title}
                        </div>
                        <div style="color:#64748b; margin-top:12px; font-size:14px;">
                            Based on the customer's demographics, services, contract and billing behavior.
                        </div>
                        <div style="margin-top:25px;">
                            <div class="result-label">CHURN PROBABILITY</div>
                            <div class="probability">{prob:.1f}%</div>
                            <div class="risk-badge {risk_class}">{risk_icon} {risk}</div>
                        </div>
                    </div>
                    """),
                    unsafe_allow_html=True,
                )

            with result_col2:
                st.markdown(
                    textwrap.dedent("""
                    <div class="result-card">
                        <div class="result-label">RISK ANALYSIS</div>
                        <div style="font-size:22px; font-weight:700; margin-top:8px;">Customer Risk Score</div>
                    </div>
                    """),
                    unsafe_allow_html=True,
                )

                st.progress(min(max(prob / 100, 0.0), 1.0), text=f"Churn probability: {prob:.1f}%")

                st.markdown(
                    textwrap.dedent("""
                    <div style="display:flex; justify-content:space-between; margin-top:15px; color:#64748b; font-size:12px;">
                        <span>Low Risk</span>
                        <span>Medium Risk</span>
                        <span>High Risk</span>
                    </div>
                    """),
                    unsafe_allow_html=True,
                )

                st.markdown("<br>", unsafe_allow_html=True)

                m1, m2 = st.columns(2)

                with m1:
                    st.markdown(
                        textwrap.dedent(f"""
                        <div class="metric-card">
                            <div class="metric-value">{tenure}</div>
                            <div class="metric-label">MONTHS WITH COMPANY</div>
                        </div>
                        """),
                        unsafe_allow_html=True,
                    )

                with m2:
                    st.markdown(
                        textwrap.dedent(f"""
                        <div class="metric-card">
                            <div class="metric-value">${monthly:.2f}</div>
                            <div class="metric-label">MONTHLY CHARGES</div>
                        </div>
                        """),
                        unsafe_allow_html=True,
                    )

            st.markdown("<br>", unsafe_allow_html=True)

            if prediction == 1:
                st.warning(
                    "⚠️ **Customer Retention Recommendation**\n\n"
                    "This customer shows elevated churn risk. "
                    "Consider reviewing their contract, service usage, pricing and support experience."
                )
            else:
                st.success(
                    "✅ **Customer Retention Status**\n\n"
                    "This customer currently shows a relatively low probability of churn based on the submitted profile."
                )
            st.divider()

            # --- 🔍 EXPLAINABLE AI SECTION ---
            st.header("🔍 Model Interpretability & Explainability (XAI)")
            
            tab1, tab2 = st.tabs(["⚡ SHAP Feature Attribution", "🧪 LIME Local Explanation"])

            with tab1:
                st.subheader("SHAP Waterfall Plot")
                st.write("Shows how each customer feature pushes the risk prediction higher (red) or lower (blue) relative to the baseline.")
                
                # Render SHAP Matplotlib figure inside Streamlit
                fig = explainer.get_shap_waterfall_plot(X_transformed)
                st.pyplot(fig, clear_figure=True)

            with tab2:
                st.subheader("LIME Explanation")
                st.write("Local Interpretable Model-agnostic Explanations (LIME) builds a local linear model to explain this individual decision.")
                
                # Load sample reference training dataset for LIME baseline
                sample_train = pd.read_csv("data/processed/train.csv")
                X_train_transformed, _ = preprocessor.transform(sample_train.head(100))
                
                lime_exp = explainer.get_lime_explanation(X_train_transformed, X_transformed)
                
                # Render HTML component for LIME
                html_content = lime_exp.as_html()
                components.html(html_content, height=500, scrolling=True)

        else:
            try:
                detail = response.json().get("detail", "Unknown API error")
            except Exception:
                detail = response.text

            st.error(f"⚠️ Prediction API Error: {detail}")

    except requests.exceptions.ConnectionError:
        st.error(
            f"🔌 **Unable to connect to the prediction server.**\n\n"
            f"Make sure your FastAPI backend is running at: `{API_URL}`"
        )
    except requests.exceptions.Timeout:
        st.error(
            "⏱️ **Prediction request timed out.**\n\n"
            "The backend took too long to respond. Please check your FastAPI service."
        )
    except Exception as e:
        st.error(f"❌ **Unexpected error**\n\n`{e}`")

st.markdown(
    textwrap.dedent("""
    <div class="footer">
        ChurnAI • AI-Powered Customer Analytics<br>
        FastAPI + Machine Learning + Streamlit
    </div>
    """),
    unsafe_allow_html=True,
)