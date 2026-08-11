import os
import requests
import streamlit as st

# Backend API configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="🔮",
    layout="wide",
)

st.title("🔮 Customer Churn Prediction Dashboard")
st.markdown(
    "Enter customer demographics, account details, and subscription services to predict churn probability."
)

st.divider()

# Input Form
with st.form("churn_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("👤 Demographics")
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior = st.selectbox("Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        tenure = st.number_input("Tenure (Months)", min_value=0, max_value=120, value=12)

    with col2:
        st.subheader("📞 Services Subscribed")
        phone = st.selectbox("Phone Service", ["Yes", "No"])
        multiple = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
        internet = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
        security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
        device = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        tech = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
        movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])

    with col3:
        st.subheader("💳 Account & Billing")
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ],
        )
        monthly = st.number_input("Monthly Charges ($)", min_value=0.0, value=70.35, step=0.5)
        total = st.number_input("Total Charges ($)", min_value=0.0, value=844.20, step=1.0)

    submit_button = st.form_submit_button(label="🚀 Predict Churn Probability", use_container_width=True)

# Prediction Request Logic
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
        with st.spinner("Analyzing customer risk profile..."):
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()
            prob = result["churn_probability"] * 100
            risk = result["risk_level"]

            st.divider()
            st.subheader("📊 Prediction Results")

            res_col1, res_col2 = st.columns(2)

            with res_col1:
                if result["churn_prediction"] == 1:
                    st.error(f"### Result: High Probability of Churn")
                else:
                    st.success(f"### Result: Low Probability of Churn")

            with res_col2:
                st.metric(label="Churn Probability", value=f"{prob:.1f}%")
                st.caption(f"Risk Level: **{risk}**")

        else:
            st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")

    except Exception as e:
        st.error(f"Could not connect to FastAPI server at {API_URL}. Exception: {e}")