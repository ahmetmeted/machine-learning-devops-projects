"""
Unit tests for the FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from model import CensusModel


# Create test client
client = TestClient(app)


def setup_module():
    """Set up the model for testing."""
    # Load or train model for testing
    try:
        model = CensusModel()
        model.load_model("model/model.pkl", "model/encoders.pkl")
    except Exception:
        # If model files don't exist, train a new one
        from train_model import train_model
        model, _ = train_model()


def test_root_endpoint():
    """Test the root GET endpoint."""
    response = client.get("/")

    # Check status code
    assert response.status_code == 200

    # Check response content
    data = response.json()
    assert "message" in data
    assert "Welcome to the Census Income Prediction API!" in data["message"]
    assert "endpoints" in data
    assert "GET /" in data["endpoints"]
    assert "POST /predict" in data["endpoints"]


def test_predict_income_high():
    """Test POST endpoint with data that should predict high income."""
    # Sample data that should predict >50K
    test_data = {
        "age": 45,
        "workclass": "Private",
        "fnlgt": 2334,
        "education": "Bachelors",
        "education-num": 13,
        "marital-status": "Married-civ-spouse",
        "occupation": "Exec-managerial",
        "relationship": "Husband",
        "race": "White",
        "sex": "Male",
        "capital-gain": 15000,
        "capital-loss": 0,
        "hours-per-week": 40,
        "native-country": "United-States"
    }

    response = client.post("/predict", json=test_data)

    # Check status code
    assert response.status_code == 200

    # Check response content
    data = response.json()
    assert "prediction" in data
    assert "prediction_label" in data
    assert data["prediction"] in [0, 1]
    assert data["prediction_label"] in ["<=50K", ">50K"]


def test_predict_income_low():
    """Test POST endpoint with data that should predict low income."""
    # Sample data that should predict <=50K
    test_data = {
        "age": 25,
        "workclass": "Private",
        "fnlgt": 1234,
        "education": "HS-grad",
        "education-num": 9,
        "marital-status": "Never-married",
        "occupation": "Handlers-cleaners",
        "relationship": "Not-in-family",
        "race": "Black",
        "sex": "Female",
        "capital-gain": 0,
        "capital-loss": 0,
        "hours-per-week": 20,
        "native-country": "United-States"
    }

    response = client.post("/predict", json=test_data)

    # Check status code
    assert response.status_code == 200

    # Check response content
    data = response.json()
    assert "prediction" in data
    assert "prediction_label" in data
    assert data["prediction"] in [0, 1]
    assert data["prediction_label"] in ["<=50K", ">50K"]


def test_predict_invalid_data():
    """Test POST endpoint with invalid data."""
    # Invalid data (missing required fields)
    test_data = {
        "age": 45,
        "workclass": "Private"
        # Missing other required fields
    }

    response = client.post("/predict", json=test_data)

    # Should return validation error
    assert response.status_code == 422


def test_predict_wrong_types():
    """Test POST endpoint with wrong data types."""
    # Wrong data types
    test_data = {
        "age": "not_a_number",
        "workclass": "Private",
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

    response = client.post("/predict", json=test_data)

    # Should return validation error
    assert response.status_code == 422


def test_predict_edge_cases():
    """Test POST endpoint with edge case values."""
    # Edge case: very high age
    test_data = {
        "age": 90,
        "workclass": "Private",
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

    response = client.post("/predict", json=test_data)

    # Should still work
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "prediction_label" in data


def test_api_docs():
    """Test that API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema():
    """Test that OpenAPI schema is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    # Check that schema contains our endpoints
    schema = response.json()
    assert "/" in schema["paths"]
    assert "/predict" in schema["paths"]
    assert "post" in schema["paths"]["/predict"]


if __name__ == "__main__":
    pytest.main([__file__])
