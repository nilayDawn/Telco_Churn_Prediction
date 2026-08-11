from pathlib import Path

import joblib
import pandas as pd

from src.utils.logger import logger


class FeatureEngineeredPreprocessor:

    def __init__(self, config: dict):
        self.config = config
        self.feature_names = None

    def fit_transform(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        """Cleans, encodes train features, and separates target column."""
        logger.info("Starting feature engineering and data preprocessing...")
        df = df.copy()

        # 1. Drop customerID
        if "customerID" in df.columns:
            df = df.drop(columns=["customerID"])

        # 2. Fix TotalCharges data type and drop missing rows
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
        df = df.dropna(subset=["TotalCharges"])

        # 3. Target Encoding (Churn: Yes -> 1, No -> 0)
        target_col = self.config["data"]["target_column"]
        if target_col in df.columns:
            if df[target_col].dtype == "object":
                df[target_col] = df[target_col].map({"Yes": 1, "No": 0})
            y = df[target_col]
            X = df.drop(columns=[target_col])
        else:
            raise KeyError(f"Target column '{target_col}' not found in data.")

        # 4. Binary Feature Mapping
        binary_cols = [
            "gender",
            "Partner",
            "Dependents",
            "PhoneService",
            "PaperlessBilling",
        ]
        binary_map = {"Yes": 1, "No": 0, "Male": 1, "Female": 0}
        for col in binary_cols:
            if col in X.columns and X[col].dtype == "object":
                X[col] = X[col].map(binary_map)

        # 5. One-Hot Encoding multi-categorical columns
        multi_cat_cols = [
            "MultipleLines",
            "InternetService",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies",
            "Contract",
            "PaymentMethod",
        ]
        existing_multi = [col for col in multi_cat_cols if col in X.columns]
        X = pd.get_dummies(X, columns=existing_multi, drop_first=True)

        # Convert boolean columns to integer (1 / 0)
        bool_cols = X.select_dtypes(include="bool").columns
        X[bool_cols] = X[bool_cols].astype(int)

        # Store engineered feature column names to align test/inference data
        self.feature_names = list(X.columns)

        logger.info(
            f"Preprocessing complete. Total features created: {len(self.feature_names)}"
        )
        return X, y

    def transform(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series | None]:
        """Transforms unseen test or inference data to match trained feature structure."""
        logger.info("Transforming new evaluation/inference dataset...")
        df = df.copy()

        if "customerID" in df.columns:
            df = df.drop(columns=["customerID"])

        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
        df["TotalCharges"] = df["TotalCharges"].fillna(0)

        target_col = self.config["data"]["target_column"]
        if target_col in df.columns:
            if df[target_col].dtype == "object":
                df[target_col] = df[target_col].map({"Yes": 1, "No": 0})
            y = df[target_col]
            X = df.drop(columns=[target_col])
        else:
            y = None
            X = df

        binary_cols = [
            "gender",
            "Partner",
            "Dependents",
            "PhoneService",
            "PaperlessBilling",
        ]
        binary_map = {"Yes": 1, "No": 0, "Male": 1, "Female": 0}
        for col in binary_cols:
            if col in X.columns and X[col].dtype == "object":
                X[col] = X[col].map(binary_map)

        multi_cat_cols = [
            "MultipleLines",
            "InternetService",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies",
            "Contract",
            "PaymentMethod",
        ]
        existing_multi = [col for col in multi_cat_cols if col in X.columns]
        X = pd.get_dummies(X, columns=existing_multi, drop_first=True)

        bool_cols = X.select_dtypes(include="bool").columns
        X[bool_cols] = X[bool_cols].astype(int)

        # Reindex features so columns exactly match training data
        if self.feature_names is not None:
            X = X.reindex(columns=self.feature_names, fill_value=0)

        return X, y

    def save_preprocessor(self):
        """Saves preprocessor metadata object to artifacts directory."""
        artifact_dir = Path(self.config["artifacts"]["model_dir"])
        artifact_dir.mkdir(parents=True, exist_ok=True)
        save_path = artifact_dir / self.config["artifacts"]["preprocessor_name"]

        joblib.dump(self, save_path)
        logger.info(f"Preprocessor object saved to {save_path}")

    @staticmethod
    def load_preprocessor(path: str):
        """Loads fitted preprocessor from path."""
        logger.info(f"Loading preprocessor from {path}")
        return joblib.load(path)