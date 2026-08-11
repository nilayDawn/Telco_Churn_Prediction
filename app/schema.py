from typing import Literal
from pydantic import BaseModel, Field


class ChurnInputSchema(BaseModel):
    gender: Literal["Male", "Female"] = Field(..., example="Female")
    SeniorCitizen: Literal[0, 1] = Field(..., example=0)
    Partner: Literal["Yes", "No"] = Field(..., example="Yes")
    Dependents: Literal["Yes", "No"] = Field(..., example="No")
    tenure: int = Field(..., ge=0, example=12)
    PhoneService: Literal["Yes", "No"] = Field(..., example="Yes")
    MultipleLines: Literal["Yes", "No", "No phone service"] = Field(
        ..., example="No"
    )
    InternetService: Literal["DSL", "Fiber optic", "No"] = Field(
        ..., example="Fiber optic"
    )
    OnlineSecurity: Literal["Yes", "No", "No internet service"] = Field(
        ..., example="No"
    )
    OnlineBackup: Literal["Yes", "No", "No internet service"] = Field(
        ..., example="Yes"
    )
    DeviceProtection: Literal["Yes", "No", "No internet service"] = Field(
        ..., example="No"
    )
    TechSupport: Literal["Yes", "No", "No internet service"] = Field(
        ..., example="No"
    )
    StreamingTV: Literal["Yes", "No", "No internet service"] = Field(
        ..., example="Yes"
    )
    StreamingMovies: Literal["Yes", "No", "No internet service"] = Field(
        ..., example="No"
    )
    Contract: Literal["Month-to-month", "One year", "Two year"] = Field(
        ..., example="Month-to-month"
    )
    PaperlessBilling: Literal["Yes", "No"] = Field(..., example="Yes")
    PaymentMethod: Literal[
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)",
    ] = Field(..., example="Electronic check")
    MonthlyCharges: float = Field(..., ge=0, example=70.35)
    TotalCharges: float = Field(..., ge=0, example=844.20)


class ChurnPredictionResponse(BaseModel):
    churn_prediction: int = Field(
        ..., description="0 for No Churn, 1 for Churn"
    )
    churn_probability: float = Field(
        ..., description="Predicted probability of churning"
    )
    risk_level: str = Field(
        ..., description="Risk category: High Risk, Medium Risk, Low Risk"
    )