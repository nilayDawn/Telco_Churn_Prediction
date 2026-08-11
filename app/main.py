from fastapi import FastAPI, HTTPException, status
import pandas as pd
from app.schema import ChurnInputSchema, ChurnPredictionResponse
from src.models.predict import ChurnPredictor
from src.utils.logger import logger
import yaml

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Production-grade API for predicting customer churn probabilities using LightGBM",
    version="1.0.0",
)

# Global predictor instance
predictor = None

def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


@app.on_event("startup")
def load_artifacts():
    global predictor
    try:
        config = load_config()
        logger.info("Initializing prediction artifacts for FastAPI server...")
        predictor = ChurnPredictor(config)
        logger.info("FastAPI initialization complete.")
    except Exception as e:
        logger.error(f"Failed to load artifacts on startup: {str(e)}")


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Health check endpoint for container orchestrators."""
    if predictor is None:
        raise HTTPException(
            status_code=503, detail="Model artifacts not loaded."
        )
    return {"status": "healthy", "model_loaded": True}


@app.post(
    "/predict",
    response_model=ChurnPredictionResponse,
    status_code=status.HTTP_200_OK,
)
def predict_churn(payload: ChurnInputSchema):
    """Predict churn for a single customer payload."""
    if predictor is None:
        raise HTTPException(
            status_code=503, detail="Model predictor service unavailable."
        )

    try:
        # Convert schema instance to Pandas DataFrame
        data_dict = payload.model_dump()
        input_df = pd.DataFrame([data_dict])

        # Run inference
        results_df = predictor.predict(input_df)

        pred = int(results_df["churn_prediction"].iloc[0])
        prob = float(results_df["churn_probability"].iloc[0])

        # Categorize risk levels
        if prob >= 0.7:
            risk = "High Risk"
        elif prob >= 0.4:
            risk = "Medium Risk"
        else:
            risk = "Low Risk"

        return ChurnPredictionResponse(
            churn_prediction=pred, churn_probability=prob, risk_level=risk
        )

    except Exception as e:
        logger.error(f"Inference error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Inference processing failed: {str(e)}"
        )