# Dynamic Risk Assessment System

A comprehensive machine learning system for predicting corporate client attrition risk with automated monitoring, retraining, and deployment capabilities.

## 🎯 Project Goals
- Implement end-to-end MLOps pipeline for production systems
- Demonstrate automated model retraining and deployment
- Showcase comprehensive monitoring and diagnostics
- Create production-ready risk assessment systems
- Implement automated data ingestion and processing

## Overview

This system provides a complete end-to-end solution for:
- **Data Ingestion**: Automatically detecting and combining new data sources
- **Model Training**: Training logistic regression models for attrition prediction
- **Model Scoring**: Evaluating model performance using F1 score
- **Model Deployment**: Deploying models to production
- **Diagnostics**: Monitoring data quality, model performance, and system health
- **Reporting**: Generating visualizations and comprehensive reports
- **API Endpoints**: RESTful API for model predictions and diagnostics
- **Process Automation**: Automated retraining and deployment based on data drift

## Project Structure

```
dynamic-risk-assessment-system/
├── config.json                 # Configuration file
├── requirements.txt            # Python dependencies
├── ingestion.py               # Data ingestion script
├── training.py                # Model training script
├── scoring.py                 # Model scoring script
├── deployment.py              # Model deployment script
├── diagnostics.py             # Diagnostics and monitoring
├── reporting.py               # Report generation
├── app.py                     # Flask API endpoints
├── apicalls.py                # API testing script
├── fullprocess.py             # Full automation pipeline
├── wsgi.py                    # WSGI configuration
├── cronjob.txt                # Cron job configuration
├── practicedata/              # Practice datasets
├── sourcedata/                # Production datasets
├── testdata/                  # Test datasets
├── ingesteddata/              # Processed data
├── models/                    # Trained models
├── practicemodels/            # Practice models
└── production_deployment/     # Production models
```

## Features

### 1. Data Ingestion (`ingestion.py`)
- Automatically detects CSV files in the input directory
- Combines multiple datasets into a single DataFrame
- Removes duplicate records
- Saves processed data and ingestion records

### 2. Model Training (`training.py`)
- Trains logistic regression models for attrition prediction
- Uses features: lastmonth_activity, lastyear_activity, number_of_employees
- Implements train-test split with stratification
- Saves trained models in pickle format

### 3. Model Scoring (`scoring.py`)
- Evaluates model performance using F1 score
- Tests models on separate test datasets
- Saves performance metrics for monitoring

### 4. Model Deployment (`deployment.py`)
- Copies trained models to production directory
- Deploys model artifacts and metadata
- Ensures production readiness

### 5. Diagnostics (`diagnostics.py`)
- **Model Predictions**: Generates predictions for new data
- **Summary Statistics**: Calculates mean, median, std for numeric columns
- **Missing Data Analysis**: Identifies data quality issues
- **Performance Timing**: Measures ingestion and training times
- **Dependency Checking**: Monitors package versions

### 6. Reporting (`reporting.py`)
- Generates confusion matrix visualizations
- Creates comprehensive PDF reports
- Includes model metrics, diagnostics, and visualizations

### 7. API Endpoints (`app.py`)
- `/prediction`: Get model predictions for input data
- `/scoring`: Retrieve current model performance
- `/summarystats`: Get data summary statistics
- `/diagnostics`: Get system diagnostics and health metrics

### 8. Process Automation (`fullprocess.py`)
- Monitors for new data availability
- Detects model drift using performance comparison
- Automatically retrains models when needed
- Deploys updated models to production
- Runs comprehensive diagnostics and reporting

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dynamic-risk-assessment-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Manual Execution

1. **Data Ingestion**:
```bash
python ingestion.py
```

2. **Model Training**:
```bash
python training.py
```

3. **Model Scoring**:
```bash
python scoring.py
```

4. **Model Deployment**:
```bash
python deployment.py
```

5. **Generate Reports**:
```bash
python reporting.py
```

6. **Run Full Pipeline**:
```bash
python fullprocess.py
```

### API Usage

1. **Start the API server**:
```bash
python app.py
```

2. **Test API endpoints**:
```bash
python apicalls.py
```

### Automated Execution

Set up the cron job to run every 10 minutes:
```bash
# Add to crontab
crontab -e

# Add this line:
*/10 * * * * cd /workspace/dynamic-risk-assessment-system && python fullprocess.py >> /workspace/dynamic-risk-assessment-system/cron.log 2>&1
```

## 🐳 Docker Usage

```bash
# Build and run with Docker
docker build -f ../docker/Dockerfile -t risk-assessment .
docker run -p 5000:5000 risk-assessment

# Or use Docker Compose
docker-compose -f ../docker/docker-compose.yml up risk-assessment
```

## Configuration

Edit `config.json` to customize paths and settings:

```json
{
    "input_folder_path": "sourcedata",
    "output_folder_path": "ingesteddata",
    "test_data_path": "testdata",
    "output_model_path": "models",
    "prod_deployment_path": "production_deployment"
}
```

## Data Format

The system expects CSV files with the following columns:
- `corporation`: Corporation identifier (not used in modeling)
- `lastmonth_activity`: Activity level in the last month
- `lastyear_activity`: Activity level in the last year
- `number_of_employees`: Number of employees
- `exited`: Target variable (1 = exited, 0 = not exited)

## Model Performance

The system uses F1 score as the primary performance metric and automatically retrains models when performance degrades (model drift detection).

## Monitoring

The system provides comprehensive monitoring through:
- Data quality metrics (missing values, summary statistics)
- Model performance tracking
- System performance timing
- Dependency version monitoring
- Automated alerting through the full process pipeline

## Output Files

- `finaldata.csv`: Combined and processed training data
- `ingestedfiles.txt`: Record of ingested files
- `trainedmodel.pkl`: Trained machine learning model
- `latestscore.txt`: Current model F1 score
- `confusionmatrix.png`: Model performance visualization
- `model_report.pdf`: Comprehensive model report
- `apireturns.txt`: API endpoint responses

## Logging

All scripts include comprehensive logging for monitoring and debugging. Logs are written to the console and can be redirected to files for production use.

## Requirements

- Python 3.8+
- pandas
- numpy
- scikit-learn
- flask
- matplotlib
- seaborn
- reportlab

## License

This project is licensed under the MIT License - see the LICENSE file for details.