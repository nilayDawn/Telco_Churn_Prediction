import pandas as pd

from src.utils.logger import logger


class DataValidator:

    def __init__(self, config: dict):
        self.config = config
        self.required_columns = [
            "customerID",
            "gender",
            "SeniorCitizen",
            "Partner",
            "Dependents",
            "tenure",
            "PhoneService",
            "MultipleLines",
            "InternetService",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies",
            "Contract",
            "PaperlessBilling",
            "PaymentMethod",
            "MonthlyCharges",
            "TotalCharges",
            "Churn",
        ]

    def validate_raw_schema(self, df: pd.DataFrame) -> bool:
        """Validates that all expected raw columns exist and the dataframe is not empty."""
        logger.info("Validating raw data schema...")

        if df.empty:
            logger.error("Raw dataframe is empty.")
            raise ValueError("Raw dataframe is empty.")

        missing_cols = [
            col for col in self.required_columns if col not in df.columns
        ]
        if missing_cols:
            logger.error(f"Missing required columns: {missing_cols}")
            raise ValueError(f"Raw data is missing columns: {missing_cols}")

        logger.info("Raw data schema validation passed successfully.")
        return True