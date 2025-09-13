# W&B Integration Summary

## ✅ Integration Complete

The NYC Airbnb price prediction pipeline has been successfully integrated with Weights & Biases (W&B) for advanced experiment tracking and model monitoring.

## 🔗 Project Links

- **GitHub Repository**: [https://github.com/your_username/build-ml-pipeline-for-short-term-rental-prices](https://github.com/your_username/build-ml-pipeline-for-short-term-rental-prices)
- **W&B Project**: [https://wandb.ai/your_entity_name/nyc_airbnb](https://wandb.ai/your_entity_name/nyc_airbnb)

## 🚀 What's Been Added

### 1. W&B Configuration
- Added W&B settings to `config.yaml`
- Project: `nyc_airbnb`
- Entity: `your_entity_name`
- API Key: Configured for authentication
- Tags: `["mlops", "airbnb", "price_prediction"]`

### 2. W&B Utilities
- Created `src/wandb_utils.py` with helper functions:
  - `init_wandb()`: Initialize W&B runs with proper configuration
  - `log_artifact()`: Log data artifacts to W&B
  - `log_model_metrics()`: Log model performance metrics
  - `log_dataframe_table()`: Log data tables for visualization

### 3. Enhanced Pipeline Integration
- **Main Pipeline** (`main.py`):
  - W&B initialization at pipeline start
  - Artifact logging after each step
  - Proper W&B session management

- **Training Step** (`src/train_random_forest/run.py`):
  - Logs training metrics (MAE, MSE, RMSE, R²)
  - Logs hyperparameters
  - Graceful handling when W&B is not initialized

- **Testing Step** (`src/test_regression_model/run.py`):
  - Logs test metrics (MAE, MSE, RMSE, R²)
  - Graceful handling when W&B is not initialized

### 4. Updated Dependencies
- Updated `environment.yml` with latest W&B version (0.16.1)
- Added `python-dotenv` for environment variable management
- Created `requirements.txt` for easy pip installation

### 5. Enhanced Documentation
- Updated `README.md` with W&B project links
- Added W&B setup instructions
- Updated configuration examples
- Added verification script (`verify_wandb.py`)

## 📊 Tracked Metrics

### Training Metrics
- `train/mae`: Mean Absolute Error on training data
- `train/mse`: Mean Squared Error on training data
- `train/rmse`: Root Mean Squared Error on training data
- `train/r2`: R-squared score on training data

### Test Metrics
- `test/mae`: Mean Absolute Error on test data
- `test/mse`: Mean Squared Error on test data
- `test/rmse`: Root Mean Squared Error on test data
- `test/r2`: R-squared score on test data

### Hyperparameters
- `hyperparameters/n_estimators`: Number of trees in Random Forest
- `hyperparameters/max_depth`: Maximum depth of trees
- `hyperparameters/max_features`: Maximum features per split
- `hyperparameters/min_samples_split`: Minimum samples to split
- `hyperparameters/min_samples_leaf`: Minimum samples per leaf
- `hyperparameters/random_seed`: Random seed for reproducibility

## 🗂️ Logged Artifacts

1. **Raw Data**: `raw_sample_data` - Original dataset
2. **Cleaned Data**: `cleaned_sample_data` - Processed dataset
3. **Training Data**: `trainval_data` - Training/validation split
4. **Test Data**: `test_data` - Test dataset
5. **Model**: `random_forest_model` - Trained Random Forest model

## 🧪 Verification

Run the verification script to ensure W&B integration is working:

```bash
python verify_wandb.py
```

This will:
- Test W&B authentication
- Create a test run
- Verify project accessibility
- Display project URL

## 🚀 Usage

### Run Complete Pipeline
```bash
python main.py
```

### Run Specific Steps
```bash
STEPS="download,basic_cleaning,data_check" python main.py
```

### Run with MLflow
```bash
mlflow run . --env-manager=local
```

## 📈 W&B Dashboard Features

The W&B project provides:
- **Experiment Tracking**: All runs with metrics and hyperparameters
- **Model Performance**: Training vs test metrics comparison
- **Artifact Management**: Versioned datasets and models
- **Visualization**: Interactive charts and tables
- **Collaboration**: Team access to experiments and results

## 🔧 Configuration

All W&B settings are in `config.yaml`:

```yaml
wandb:
  project: "nyc_airbnb"
  entity: "your_entity_name"
  api_key: "your_wandb_api_key"
  tags: ["mlops", "airbnb", "price_prediction"]
```

## ✅ Ready for Submission

The project is now ready for submission with:
- ✅ Public W&B project accessible to reviewers
- ✅ GitHub repository with complete code
- ✅ Comprehensive documentation
- ✅ Working ML pipeline with W&B integration
- ✅ All artifacts and metrics properly logged

## 🎯 Next Steps

1. **Push to GitHub**: Commit and push all changes
2. **Verify W&B Project**: Ensure project is public and accessible
3. **Submit**: Include both GitHub and W&B links in submission
4. **Monitor**: Use W&B dashboard to track future experiments
