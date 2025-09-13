# NYC Airbnb Price Prediction Pipeline

This project implements an end-to-end ML pipeline for predicting short-term rental prices in NYC using MLflow, Weights & Biases (W&B), and local file system.

## 🔗 Project Links

- **W&B Public Project**: [https://wandb.ai/your_entity_name/nyc_airbnb_public](https://wandb.ai/your_entity_name/nyc_airbnb_public) 🌐

## 🎯 Project Goals
- Implement end-to-end MLOps pipeline for production systems
- Demonstrate automated data processing and model training
- Showcase experiment tracking and model versioning
- Create reusable ML pipeline components
- Implement comprehensive monitoring and validation

## 🏠 Project Overview

This ML pipeline is designed for a property management company that rents rooms and properties for short periods. The pipeline estimates typical prices for given properties based on similar properties' prices. The model needs to be retrained weekly with new data, necessitating an end-to-end pipeline that can be reused.

## 📁 Project Structure

```
├── src/
│   ├── eda/                    # Exploratory Data Analysis (Jupyter notebook)
│   ├── basic_cleaning/         # Data cleaning step
│   ├── data_check/            # Data quality testing
│   ├── train_val_test_split/  # Data splitting
│   ├── train_random_forest/   # Model training
│   └── test_regression_model/ # Model testing
├── data/
│   └── raw/                   # Raw data files
├── artifacts/                 # Generated artifacts and models
├── main.py                   # Main pipeline orchestrator
├── config.yaml              # Configuration file
├── MLproject               # MLflow project definition
├── environment.yml         # Conda environment specification
├── run_hyperparameter_optimization.py  # Hyperparameter tuning script
└── select_best_model.py    # Model selection script
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create conda environment
conda env create -f environment.yml
conda activate nyc_airbnb_dev

# Or install dependencies directly
pip install -r requirements.txt
```

### 2. Setup Weights & Biases

```bash
# Login to W&B (optional if API key is in config)
wandb login

# Verify W&B project access
# The project is now PUBLIC: https://wandb.ai/your_entity_name/nyc_airbnb_public
```

### 3. Run the Pipeline

```bash
# Run entire pipeline with PUBLIC W&B project
python run_public_pipeline.py

# Or run with MLflow (uses public config by default)
mlflow run . --env-manager=local

# Run specific steps
mlflow run . -P steps="download,basic_cleaning,data_check" --env-manager=local

# Run with custom parameters
mlflow run . -P hydra_options="etl.min_price=50 modeling.random_forest.n_estimators=100" --env-manager=local
```

### 4. Hyperparameter Optimization

```bash
# Run hyperparameter optimization
python run_hyperparameter_optimization.py

# Select best model
python select_best_model.py
```

## 🔧 Pipeline Steps

1. **Download**: Downloads sample data from local files
2. **EDA**: Exploratory data analysis (Jupyter notebook)
3. **Basic Cleaning**: Removes outliers and cleans data
4. **Data Check**: Validates data quality with automated tests
5. **Train/Val/Test Split**: Splits data into train/validation/test sets
6. **Train Random Forest**: Trains the ML model with preprocessing
7. **Test Model**: Evaluates model performance on test set

## 📊 Data Processing

- **Input**: Raw CSV data with property information
- **Cleaning**: Removes outliers (price range: $10-$350)
- **Preprocessing**: Handles missing values, categorical encoding, text features
- **Validation**: Automated data quality checks

## 🎯 Model Features

- **Algorithm**: Random Forest Regressor
- **Text Processing**: TF-IDF vectorization for property names
- **Categorical Encoding**: One-hot encoding for categorical features
- **Missing Value Handling**: Imputation strategies for different data types
- **Hyperparameter Tuning**: Automated optimization of model parameters

## 📈 Performance Tracking

- **MLflow**: Experiment tracking and model versioning
- **Weights & Biases**: Advanced experiment tracking, metrics visualization, and model monitoring
- **Metrics**: MAE, MSE, RMSE, and R² for comprehensive model evaluation
- **Artifacts**: All models and data artifacts stored locally and logged to W&B
- **Visualization**: Pipeline lineage, experiment comparison, and interactive dashboards

## ⚙️ Configuration

### Public vs Private Configuration

The project now supports both public and private W&B configurations:

- **`config.yaml`**: Uses public W&B project (`nyc_airbnb_public`) by default
- **`config_public.yaml`**: Explicitly configured for public sharing
- **`run_public_pipeline.py`**: Script to run with public configuration

All parameters are defined in `config.yaml`:

```yaml
main:
  project_name: "nyc_airbnb"
  experiment_name: "short_term_rental_pipeline"

wandb:
  project: "nyc_airbnb_public"
  entity: "your_entity_name"
  api_key: "your_wandb_api_key"
  tags: ["mlops", "airbnb", "price_prediction", "public"]

etl:
  sample: "sample.csv"
  min_price: 10
  max_price: 350

modeling:
  test_size: 0.2
  random_seed: 42
  stratify_by: "neighbourhood_group"
  max_tfidf_features: 15
  random_forest:
    n_estimators: 200
    max_depth: null
    max_features: 0.5
    min_samples_split: 2
    min_samples_leaf: 1
```

## 🔄 Usage Examples

### Basic Pipeline Execution
```bash
# Run all steps
mlflow run . --env-manager=local

# Run specific steps
mlflow run . -P steps="download,basic_cleaning" --env-manager=local
```

### Hyperparameter Optimization
```bash
# Run optimization script
python run_hyperparameter_optimization.py

# Select best model
python select_best_model.py
```

### Custom Parameters
```bash
# Override configuration parameters
mlflow run . -P hydra_options="etl.min_price=50 modeling.random_forest.n_estimators=100" --env-manager=local
```

## 🐳 Docker Usage

```bash
# Build and run with Docker
docker build -f ../docker/Dockerfile -t ml-pipeline .
docker run -v $(pwd):/app ml-pipeline python main.py
```

## 📋 Requirements

- Python 3.9
- MLflow 2.0+
- scikit-learn 1.0.2
- pandas 1.2.3
- hydra-core 1.1.1
- jupyter (for EDA)

## 🏷️ Version History

- **v1.0.0**: Initial release with basic pipeline
- **v1.1.0**: Added hyperparameter optimization
- **v1.2.0**: Improved data validation and error handling

## 📝 License

This project is part of the Udacity MLOps Nanodegree program.

## 🤝 Contributing

This is a learning project. Feel free to fork and experiment with different approaches!