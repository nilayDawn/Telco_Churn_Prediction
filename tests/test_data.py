import pandas as pd
import pytest

from src.data.validate_data import DataValidator


@pytest.fixture
def sample_valid_data():
    """Provides a valid row of Telco dataset columns."""
    return pd.DataFrame([
        {
            "customerID": "7590-VHVEG",
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
            "TotalCharges": 29.85,
            "Churn": "No",
        }
    ])


def test_validate_raw_schema_success(sample_valid_data):
    validator = DataValidator(config={})
    assert validator.validate_raw_schema(sample_valid_data) is True


def test_validate_raw_schema_missing_column(sample_valid_data):
    invalid_df = sample_valid_data.drop(columns=["gender"])
    validator = DataValidator(config={})
    with pytest.raises(ValueError, match="missing columns"):
        validator.validate_raw_schema(invalid_df)


def test_validate_raw_schema_empty():
    empty_df = pd.DataFrame()
    validator = DataValidator(config={})
    with pytest.raises(ValueError, match="empty"):
        validator.validate_raw_schema(empty_df)