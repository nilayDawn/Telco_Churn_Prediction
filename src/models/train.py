from pathlib import Path

import matplotlib.pyplot as plt
import joblib
import lightgbm as lgb
import mlflow
import mlflow.lightgbm
import pandas as pd
import shap
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.utils.logger import logger


class ModelTrainer:

    def __init__(self, config: dict):
        self.config = config
        self.model_params = config["model"]["params"]
        self.model_dir = Path(config["artifacts"]["model_dir"])
        self.model_name = config["artifacts"]["model_name"]
        self.model = None

    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> lgb.LGBMClassifier:
        """Trains LightGBM Classifier using parameters defined in config."""
        logger.info("Initializing LightGBM classifier...")
        self.model = lgb.LGBMClassifier(**self.model_params)

        logger.info("Training LightGBM model on training dataset...")
        self.model.fit(X_train, y_train)
        logger.info("Model training completed successfully.")
        return self.model

    def evaluate(
        self, X_test: pd.DataFrame, y_test: pd.Series
    ) -> dict[str, float]:
        """Evaluates model performance metrics."""
        if self.model is None:
            raise ValueError("Model has not been trained yet.")

        logger.info("Evaluating model on test dataset...")
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred, zero_division=0)),
            "recall": float(recall_score(y_test, y_pred, zero_division=0)),
            "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
            "roc_auc": float(roc_auc_score(y_test, y_proba)),
        }

        logger.info(f"Evaluation Metrics: {metrics}")
        return metrics

    def save_model(self):
        """Saves model binary to artifacts folder."""
        if self.model is None:
            raise ValueError("No model available to save.")

        self.model_dir.mkdir(parents=True, exist_ok=True)
        save_path = self.model_dir / self.model_name
        joblib.dump(self.model, save_path)
        logger.info(f"Model saved successfully to {save_path}")

    def log_to_mlflow(self, metrics: dict[str, float]):
        """Logs parameters, evaluation metrics, and model artifact to MLflow."""
        tracking_uri = self.config["mlflow"]["tracking_uri"]
        experiment_name = self.config["mlflow"]["experiment_name"]

        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)

        with mlflow.start_run():
            logger.info("Logging run details to MLflow...")
            mlflow.log_params(self.model_params)
            mlflow.log_metrics(metrics)

            # Log trained LightGBM model artifact
            mlflow.lightgbm.log_model(self.model, artifact_path="model")
            logger.info("MLflow logging completed.")
    def log_shap_summary(model, X_train):
        explainer = shap.TreeExplainer(model)
        shap_values = explainer(X_train)

        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, X_train, show=False)
        
        plot_path = "shap_summary.png"
        plt.tight_layout()
        plt.savefig(plot_path, dpi=300)
        plt.close()

        # Log image artifact to MLflow
        mlflow.log_artifact(plot_path, artifact_path="plots")