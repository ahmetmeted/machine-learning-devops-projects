# Census Income Prediction API

A FastAPI-based machine learning API that predicts whether a person's income exceeds $50,000 based on census data.

## 🎯 Project Goals
- Demonstrate modern API development with FastAPI
- Implement machine learning model deployment to cloud platforms
- Showcase CI/CD best practices for ML applications
- Create production-ready cloud applications
- Implement comprehensive testing and monitoring

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Machine Learning Model**: Random Forest classifier trained on census data
- **Interactive Documentation**: Automatic API documentation with Swagger UI
- **Type Hints**: Full Python type hints for better code quality
- **Pydantic Models**: Data validation and serialization
- **Comprehensive Testing**: Unit tests for both API and model
- **CI/CD Pipeline**: GitHub Actions for automated testing and deployment
- **Cloud Deployment**: Ready for deployment on Render.com

## API Endpoints

### GET /
Returns a welcome message and API information.

**Response:**
```json
{
  "message": "Welcome to the Census Income Prediction API!",
  "description": "This API predicts whether a person's income exceeds $50,000 based on census data.",
  "endpoints": {
    "GET /": "This welcome message",
    "POST /predict": "Make income predictions",
    "GET /docs": "Interactive API documentation"
  }
}
```

### POST /predict
Predicts income based on census data.

**Request Body:**
```json
{
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
```

**Response:**
```json
{
  "prediction": 1,
  "prediction_label": ">50K"
}
```

### GET /docs
Interactive API documentation (Swagger UI).

### GET /openapi.json
OpenAPI schema definition.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ml_model_to_cloud_application_platform_with_FastAPI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train the model (if not already trained):
```bash
python train_model.py
```

4. Run the API:
```bash
python main.py
```

The API will be available at `http://localhost:8000`.

## Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test files
pytest test_api.py
pytest test_model.py
```

## Code Quality

The project uses flake8 for code quality checks:
```bash
flake8 .
```

## 🐳 Docker Usage

```bash
# Build and run with Docker
docker build -f ../docker/Dockerfile -t fastapi-app .
docker run -p 8000:8000 fastapi-app

# Or use Docker Compose
docker-compose -f ../docker/docker-compose.yml up fastapi-app
```

## Deployment

### Render.com Deployment

1. Connect your GitHub repository to Render.com
2. Create a new Web Service
3. Configure the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Python Version**: 3.9
4. Enable Auto-Deploy for continuous deployment

### Environment Variables

No environment variables are required for basic functionality.

## Project Structure

```
├── main.py                 # FastAPI application
├── model.py               # Machine learning model implementation
├── train_model.py         # Model training script
├── test_api.py           # API tests
├── test_model.py         # Model tests
├── test_live_api.py      # Live API testing script
├── requirements.txt      # Python dependencies
├── Procfile             # Render.com deployment configuration
├── .github/workflows/   # GitHub Actions CI/CD
├── model/               # Trained model files
├── census.csv          # Training data
└── README.md           # This file
```

## Screenshots

The project includes several screenshots demonstrating functionality:

- `live_get.png`: Live GET endpoint test result
- `live_post.png`: Live POST endpoint test result
- `example.png`: API documentation with examples
- `continuous_integration.png`: CI/CD pipeline passing
- `continuous_deloyment.png`: Deployment configuration

## Model Performance

The Random Forest model achieves the following performance metrics:
- **Accuracy**: ~85%
- **Precision**: ~85%
- **Recall**: ~85%
- **F1-Score**: ~85%

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- UCI Machine Learning Repository for the census dataset
- FastAPI for the excellent web framework
- scikit-learn for machine learning tools