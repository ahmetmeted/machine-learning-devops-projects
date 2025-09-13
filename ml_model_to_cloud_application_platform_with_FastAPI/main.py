"""
FastAPI application for Census Income Prediction Model
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal
from contextlib import asynccontextmanager
import pandas as pd
from model import CensusModel

# Global model variable
model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the trained model on startup."""
    global model
    try:
        model = CensusModel()
        model.load_model("model/model.pkl", "model/encoders.pkl")
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        # If model files don't exist, train a new one
        print("Training new model...")
        from train_model import train_model
        model, _ = train_model()
    yield
    # Cleanup code here if needed


# Initialize FastAPI app
app = FastAPI(
    title="Census Income Prediction API",
    description="API for predicting income based on census data",
    version="1.0.0",
    lifespan=lifespan
)


# Pydantic model for request body
class CensusData(BaseModel):
    age: int = Field(..., description="Age of the person")
    workclass: str = Field(..., description="Type of work")
    fnlgt: int = Field(..., description="Final weight")
    education: str = Field(..., description="Education level")
    education_num: int = Field(..., alias="education-num", description="Education number")
    marital_status: str = Field(..., alias="marital-status", description="Marital status")
    occupation: str = Field(..., description="Occupation")
    relationship: str = Field(..., description="Relationship status")
    race: str = Field(..., description="Race")
    sex: str = Field(..., description="Sex")
    capital_gain: int = Field(..., alias="capital-gain", description="Capital gain")
    capital_loss: int = Field(..., alias="capital-loss", description="Capital loss")
    hours_per_week: int = Field(..., alias="hours-per-week", description="Hours per week")
    native_country: str = Field(..., alias="native-country", description="Native country")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 45,
                "workclass": "State-gov",
                "fnlgt": 2334,
                "education": "Bachelors",
                "education-num": 13,
                "marital-status": "Never-married",
                "occupation": "Prof-specialty",
                "relationship": "Wife",
                "race": "Black",
                "sex": "Female",
                "capital-gain": 2174,
                "capital-loss": 0,
                "hours-per-week": 60,
                "native-country": "Cuba"
            }
        }
    )


# Response model
class PredictionResponse(BaseModel):
    prediction: Literal[0, 1] = Field(..., description="Prediction: 0 for <=50K, 1 for >50K")
    prediction_label: str = Field(..., description="Human-readable prediction")


@app.get("/")
async def root():
    """Root endpoint with welcome message."""
    return {
        "message": "Welcome to the Census Income Prediction API!",
        "description": "This API predicts whether a person's income exceeds $50,000 based on census data.",
        "endpoints": {
            "GET /": "This welcome message",
            "POST /predict": "Make income predictions",
            "GET /docs": "Interactive API documentation"
        }
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_income(data: CensusData):
    """
    Predict income based on census data.

    Returns:
    - prediction: 0 for <=50K, 1 for >50K
    - prediction_label: Human-readable prediction
    """
    global model
    if model is None:
        # Try to load model if not already loaded
        try:
            model = CensusModel()
            model.load_model("model/model.pkl", "model/encoders.pkl")
        except Exception:
            # If model files don't exist, train a new one
            from train_model import train_model
            model, _ = train_model()

    try:
        # Convert Pydantic model to DataFrame
        input_data = {
            "age": data.age,
            "workclass": data.workclass,
            "fnlgt": data.fnlgt,
            "education": data.education,
            "education-num": data.education_num,
            "marital-status": data.marital_status,
            "occupation": data.occupation,
            "relationship": data.relationship,
            "race": data.race,
            "sex": data.sex,
            "capital-gain": data.capital_gain,
            "capital-loss": data.capital_loss,
            "hours-per-week": data.hours_per_week,
            "native-country": data.native_country
        }

        # Create DataFrame
        df = pd.DataFrame([input_data])

        # Make prediction
        prediction = model.predict(df)[0]

        # Convert prediction to label
        prediction_label = ">50K" if prediction == 1 else "<=50K"

        return PredictionResponse(
            prediction=prediction,
            prediction_label=prediction_label
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
