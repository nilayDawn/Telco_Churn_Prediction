import pandas as pd
from src.features.build_features import FeatureEngineeredPreprocessor


def test_fit_transform_pipeline():
    dummy_data = pd.DataFrame([
        {
            "customerID": "1234-TEST",
            "gender": "Female",
            "SeniorCitizen": 0,
            "Partner": "Yes",
            "Dependents": "No",
            "tenure": 12,
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "DSL",
            "OnlineSecurity": "Yes",
            "OnlineBackup": "No",
            "DeviceProtection": "Yes",
            "TechSupport": "No",
            "StreamingTV": "No",
            "StreamingMovies": "No",
            "Contract": "One year",
            "PaperlessBilling": "No",
            "PaymentMethod": "Mailed check",
            "MonthlyCharges": 50.0,
            "TotalCharges": "600.0",
            "Churn": "Yes",
        }
    ])

    config = {"data": {"target_column": "Churn"}}
    preprocessor = FeatureEngineeredPreprocessor(config)

    X, y = preprocessor.fit_transform(dummy_data)

    # Check target extraction
    assert y.iloc[0] == 1
    # Ensure customerID dropped
    assert "customerID" not in X.columns
    # Ensure binary encoding applied
    assert X["gender"].iloc[0] == 0
    # Ensure TotalCharges converted to numeric
    assert X["TotalCharges"].iloc[0] == 600.0