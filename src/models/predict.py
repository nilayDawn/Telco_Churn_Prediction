from pathlib import Path
import joblib
import pandas as pd
from src.features.build_features import FeatureEngineeredPreprocessor
from src.utils.logger import logger


class ChurnPredictor:

    def __init__(self, config: dict):
        self.model_path = Path(config["artifacts"]["model_dir"]) / config["artifacts"]["model_name"]
        self.preprocessor_path = Path(config["artifacts"]["model_dir"]) / config["artifacts"]["preprocessor_name"]
                                     
        if not self.model_path.exists() or not self.preprocessor_path.exists():
            logger.error("Artifacts missing. Please train the model first.")
            raise FileNotFoundError("Model or Preprocessor artifact not found.")

        logger.info("Loading preprocessor and LightGBM model artifacts...")
        self.preprocessor = FeatureEngineeredPreprocessor.load_preprocessor(
            str(self.preprocessor_path)
        )
        self.model = joblib.load(self.model_path)

    def predict(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """Transforms input DataFrame and predicts churn class and probability."""
        logger.info(f"Running inference on dataset with {len(input_df)} records...")

        # Transform raw features using loaded preprocessor
        X_transformed, _ = self.preprocessor.transform(input_df)

        # Make predictions
        predictions = self.model.predict(X_transformed)
        probabilities = self.model.predict_proba(X_transformed)[:, 1]

        results = input_df.copy()
        results["churn_prediction"] = predictions
        results["churn_probability"] = probabilities.round(4)

        logger.info("Inference finished successfully.")
        return results