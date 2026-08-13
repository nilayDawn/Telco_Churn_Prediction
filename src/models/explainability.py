from pathlib import Path
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from lime.lime_tabular import LimeTabularExplainer
from src.utils.logger import logger


class ModelExplainer:
    def __init__(self, model_path: str = "artifacts/model.pkl", preprocessor_path: str = "artifacts/preprocessor.pkl"):
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)
        self.feature_names = self.preprocessor.feature_names

        # 1. Initialize SHAP Explainer (Optimized for Tree-based models like LightGBM)
        self.shap_explainer = shap.TreeExplainer(self.model)

    def get_shap_waterfall_plot(self, transformed_input_df: pd.DataFrame):
        """Generates a SHAP waterfall plot for a single instance."""
        logger.info("Generating SHAP values for prediction explanation...")
        shap_values = self.shap_explainer(transformed_input_df)

        fig, ax = plt.subplots(figsize=(8, 5))
        # Generate waterfall plot for the single prediction (index 0)
        shap.plots.waterfall(shap_values[0], show=False)
        plt.tight_layout()
        return fig

    def get_lime_explanation(self, training_data_df: pd.DataFrame, instance_df: pd.DataFrame):
        """Generates a LIME explanation HTML/plot for local model interpretability."""
        logger.info("Initializing LIME Tabular Explainer...")
        
        explainer = LimeTabularExplainer(
            training_data=training_data_df.values,
            feature_names=self.feature_names,
            class_names=["Retained", "Churn"],
            mode="classification",
        )

        # Predict probability function for LIME
        predict_fn = lambda x: self.model.predict_proba(x)

        exp = explainer.explain_instance(
            data_row=instance_df.iloc[0],
            predict_fn=predict_fn,
            num_features=8
        )
        return exp