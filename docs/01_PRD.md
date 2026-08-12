# Product Requirement Document (PRD) — Telecommunications Customer Churn Prediction System

## 1. Purpose & Executive Summary
The **Customer Churn Prediction System** is designed to bridge machine learning model outputs with direct business action in telecommunications. Acquiring new customers costs 5× to 25× more than retaining existing ones. By providing real-time, actionable predictions of customer churn risk, this system enables retention teams to proactively intervene with targeted incentives, saving revenue and preserving Customer Lifetime Value (LTV).

---

## 2. Problem Statement
Customer churn in the telecommunications industry leads to substantial monthly revenue loss and decreased market share. Customers frequently churn due to high monthly charges, flexible month-to-month contracts, lack of technical support, or competitor promotions. Without an automated predictive mechanism, retention interventions are reactive (e.g., trying to win back customers after they request cancellation), which yields low conversion rates at high costs.

---

## 3. Business Goal
Identify high-risk churn customers early and accurately so retention teams and automated marketing systems can execute targeted retention workflows (e.g., offering loyalty discounts, contract upgrades, or priority support) *before* the customer decides to leave.

---

## 4. User Personas

| Persona | Primary Interface | Key Objectives & Workflow |
| :--- | :--- | :--- |
| **Retention Managers** | Streamlit Web UI (`app/frontend.py`) | <ul><li>Perform single-customer churn risk checks.</li><li>Upload batch customer data for automated scoring.</li><li>Inspect key risk factors (Monthly Charges, Tenure, Contract Type) and determine targeted retention offers.</li></ul> |
| **Automated Marketing & CRM Systems** | FastAPI REST API (`/predict`) | <ul><li>Trigger real-time risk checks upon customer profile updates or billing cycles.</li><li>Automatically assign risk tags (`High Risk`, `Medium Risk`, `Low Risk`) in CRM.</li><li>Enqueue high-risk customers into automated retention email/SMS workflows.</li></ul> |

---

## 5. Success Metrics

### 5.1 Machine Learning Metrics
* **Recall $\ge 85\%$**: Primary ML metric. High recall minimizes **False Negatives** (failing to identify a customer who actually churns), which represents the highest financial risk to the business.
* **ROC-AUC $\ge 0.85$**: Secondary ML metric. Measures the model's ability to discriminate between churners and non-churners across all possible decision thresholds.

