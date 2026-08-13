# Model Card — LightGBM Customer Churn Classifier

## 1. Model Details
* **Model Name**: LightGBM Customer Churn Classifier
* **Model Version**: `1.0.0`
* **Model Type**: Gradient Boosting Machine (LightGBM)
* **Optimization Framework**: Optuna Bayesian Optimization
* **Tracking Framework**: MLflow Experiment Tracking (`SQLite` metadata backend)
* **Primary Developer**: Telco Data Science & MLOps Team
* **Release Date**: August 2026
* **Experiment Notebook**: [`NOTEBOOKS/experiment.ipynb`](../NOTEBOOKS/experiment.ipynb)

---

## 2. Intended Use
* **Primary Intended Use**: Predict individual customer churn probability and assign churn risk levels (`High Risk`, `Medium Risk`, `Low Risk`) for telecommunications subscribers.
* **Primary Users**: Retention Managers (via Streamlit UI) and Automated Marketing/CRM Services (via FastAPI `/predict` endpoint).
* **Out-of-Scope Use Cases**: Credit scoring, fraud detection, or predicting churn for non-telecommunications subscriber bases without re-tuning.

---

## 3. Training & Validation Data
* **Dataset**: IBM Telco Customer Churn Dataset (`7,043` subscriber records).
* **Data Splits**: 80% Training set (`5,625` records), 20% Test set (`1,407` records) with stratified sampling on target variable (`Churn`).
* **Preprocessing**: Imputed missing `TotalCharges` values, categorical one-hot encoding, feature scaling, and Great Expectations schema validation checks.

---

## 4. Hyperparameters
Optimized via Optuna over 50 search trials with objective function tuned for maximum Recall score at threshold = 0.35 (reference: [`NOTEBOOKS/experiment.ipynb`](../NOTEBOOKS/experiment.ipynb)):

```yaml
n_estimators: 100
learning_rate: 0.010001
max_depth: 4
num_leaves: 21
min_child_samples: 15
subsample: 0.8417
colsample_bytree: 0.6590
class_weight: "balanced"
```

---

## 5. Model Evaluation & Metrics (Test Set)

Evaluation metrics computed on the unseen test set ($N = 1,407$):

| Metric | Score | Business Interpretation |
| :--- | :--- | :--- |
| **Recall (Churn = 1)** | **$94.38\%$** | Identifies $\approx 95\%$ of true churners (356 out of 374), minimizing costly False Negatives. |
| **Precision (Churn = 1)** | **$67.33`\%$** | Reflects broad screening policy; flags potential churners for targeted retention offers. |
| **F1-Score (Churn = 1)** | **$58.73\%$** | Harmonic mean of precision and recall under high-recall optimization. |
| **Accuracy** | **$59.06\%$** | Overall classification accuracy under class-weighted recall-prioritized threshold ($0.35$). |
| **Inference Latency** | **$2.3\text{ ms}$** | Ultra low-latency inference suitable for real-time CRM API integration. |

---

## 6. Model Performance vs Baselines

Comparison of candidate architectures evaluated in [`NOTEBOOKS/experiment.ipynb`](../NOTEBOOKS/experiment.ipynb):

| Model Architecture | Operating Thresh | Recall | Precision | F1-Score | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest Baseline** | $0.40$ | $75.9\%$ | $50.2\%$ | $0.604$ | $60.0\text{ ms}$ |
| **XGBoost Classifier** | $0.40$ | $75.9\%$ | $50.3\%$ | $0.605$ | $25.7\text{ ms}$ |
| **LightGBM (Default Baseline)** | $0.35$ | $79.7\%$ | $50.1\%$ | $0.615$ | $7.7\text{ ms}$ |
| **LightGBM (Optuna Tuned)** | **$0.35$** | **$95.2\%$** | **$38.2\%$** | **$0.545$** | **$2.3\text{ ms}$** |

---

## 7. Limitations & Bias

1. **Contract Type Sensitivity**: The model relies heavily on `Contract` type (Month-to-month vs 1-Year/2-Year). Customers on month-to-month contracts receive higher baseline risk scores.
2. **Demographic Assumptions**: Trained on Western telecommunications demographic patterns; may require re-calibration when deployed to international or prepaid subscriber markets.
3. **Recall-Precision Trade-off**: Prioritizing ultra-high recall ($95.2\%$) means accepting lower precision ($38.2\%$). Some customers flagged as high risk will remain subscribers even without intervention.
