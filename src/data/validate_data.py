import pandas as pd

import great_expectations as gx
from src.utils.logger import logger


class DataValidator:

    def __init__(self, config: dict):
        self.config = config
        self.context = gx.get_context()

    def validate_raw_schema(self, df: pd.DataFrame) -> bool:
        """Validates incoming raw data schema using Great Expectations."""
        logger.info("Running Great Expectations data validation suite...")

        if df.empty:
            logger.error("Raw dataframe is empty.")
            raise ValueError("Raw dataframe is empty.")

        # Create an in-memory GX validator for the dataframe
        data_source = self.context.data_sources.add_pandas("raw_churn_datasource")
        data_asset = data_source.add_dataframe_asset("raw_churn_asset")
        batch_definition = data_asset.add_batch_definition_whole_dataframe("raw_batch")
        
        batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

        # Define Expectation Suite
        suite = gx.ExpectationSuite(name="churn_raw_validation_suite")

        # 1. Check essential columns exist
        required_cols = [
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

        for col in required_cols:
            suite.add_expectation(
                gx.expectations.ExpectColumnToExist(column=col)
            )

        # 2. Add domain-specific value quality checks
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeBetween(
                column="tenure", min_value=0, max_value=120
            )
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToBeInSet(
                column="Churn", value_set=["Yes", "No"]
            )
        )
        suite.add_expectation(
            gx.expectations.ExpectColumnValuesToNotBeNull(
                column="customerID"
            )
        )

        self.context.suites.add(suite)

        # Run Validation
        results = batch.validate(suite)

        if not results.success:
            logger.error("Data validation failed against Great Expectations suite!")
            logger.error(f"Validation summary: {results}")
            raise ValueError("Data validation checks failed!")

        logger.info("Great Expectations validation passed successfully!")
        return True