# REST API Documentation — Customer Churn Prediction API

## 1. Overview
The **Customer Churn Prediction API** is built using FastAPI and Pydantic to provide asynchronous, schema-validated, low-latency churn inference. 

* **Base URL**: `http://localhost:8000` (or `http://churn-api:8000` inside Docker environment)
* **API Documentation**: Interactive Swagger UI available at `http://localhost:8000/docs`
* **OpenAPI Schema**: `http://localhost:8000/openapi.json`

---

## 2. Endpoints Technical Reference

### 2.1 GET `/health`
Check the API server health status and verify model predictor initialization.

#### Request
```http
GET /health HTTP/1.1
Host: localhost:8000
Accept: application/json
```

#### Success Response (`200 OK`)
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

#### Error Response (`503 Service Unavailable`)
```json
{
  "detail": "Model artifacts not loaded."
}
```

---

### 2.2 POST `/predict`
Predict churn probability and return qualitative risk category for a single customer payload.

#### Request
```http
POST /predict HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 1,
  "PhoneService": "No",
  "MultipleLines": "No phone service",
  "InternetService": "DSL",
  "OnlineSecurity": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 29.85,
  "TotalCharges": 29.85
}
```

#### Field Specifications (`ChurnInputSchema`)

| Field Name | Type | Allowed Values / Constraints | Example |
| :--- | :--- | :--- | :--- |
| `gender` | String | `"Male"`, `"Female"` | `"Female"` |
| `SeniorCitizen` | Integer | `0`, `1` | `0` |
| `Partner` | String | `"Yes"`, `"No"` | `"Yes"` |
| `Dependents` | String | `"Yes"`, `"No"` | `"No"` |
| `tenure` | Integer | $\ge 0$ | `1` |
| `PhoneService` | String | `"Yes"`, `"No"` | `"No"` |
| `MultipleLines` | String | `"Yes"`, `"No"`, `"No phone service"` | `"No phone service"` |
| `InternetService` | String | `"DSL"`, `"Fiber optic"`, `"No"` | `"DSL"` |
| `OnlineSecurity` | String | `"Yes"`, `"No"`, `"No internet service"` | `"No"` |
| `OnlineBackup` | String | `"Yes"`, `"No"`, `"No internet service"` | `"Yes"` |
| `DeviceProtection` | String | `"Yes"`, `"No"`, `"No internet service"` | `"No"` |
| `TechSupport` | String | `"Yes"`, `"No"`, `"No internet service"` | `"No"` |
| `StreamingTV` | String | `"Yes"`, `"No"`, `"No internet service"` | `"No"` |
| `StreamingMovies` | String | `"Yes"`, `"No"`, `"No internet service"` | `"No"` |
| `Contract` | String | `"Month-to-month"`, `"One year"`, `"Two year"` | `"Month-to-month"` |
| `PaperlessBilling` | String | `"Yes"`, `"No"` | `"Yes"` |
| `PaymentMethod` | String | `"Electronic check"`, `"Mailed check"`, `"Bank transfer (automatic)"`, `"Credit card (automatic)"` | `"Electronic check"` |
| `MonthlyCharges` | Float | $\ge 0.0$ | `29.85` |
| `TotalCharges` | Float | $\ge 0.0$ | `29.85` |

#### Success Response (`200 OK`)
```json
{
  "churn_prediction": 1,
  "churn_probability": 0.742,
  "risk_level": "High Risk"
}
```

#### Risk Threshold Mapping

| Predicted Probability ($p$) | Risk Level Output | Business Action Recommendation |
| :--- | :--- | :--- |
| $p \ge 0.70$ | `High Risk` | Immediate high-touch retention offer (e.g. 20% discount + contract upgrade). |
| $0.40 \le p < 0.70$ | `Medium Risk` | Trigger automated email campaign offering free add-on services or tech check. |
| $p < 0.40$ | `Low Risk` | Standard customer lifecycle communication; no proactive incentive required. |

#### Error Response (`422 Unprocessable Entity`)
Returned when payload validation fails (e.g. invalid string literal or missing field):
```json
{
  "detail": [
    {
      "loc": ["body", "Contract"],
      "msg": "value is not a valid enumeration member",
      "type": "type_error.enum"
    }
  ]
}
```
