import argparse
import os
import mlflow
import pandas as pd
import joblib
import logging
import wandb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

TARGET = "price"

# Initialize W&B if not already initialized
try:
    if not wandb.run:
        wandb.init(
            project="nyc_airbnb_public",
            entity="your_entity_name",
            name="test_run",
            tags=["test", "evaluation"]
        )
except:
    # W&B not available, continue without it
    pass

ap = argparse.ArgumentParser()
ap.add_argument("--model_uri", required=True, type=str, help="Model URI or path")
ap.add_argument("--test_csv", required=True, type=str, help="Test CSV file path")
args = ap.parse_args()

logger.info("Reading test data")
df = pd.read_csv(args.test_csv)
X = df.drop(columns=[TARGET])
y = df[TARGET]

logger.info("Loading model")
model_path = os.path.join(args.model_uri, "model.joblib")
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = mlflow.sklearn.load_model(args.model_uri)

logger.info("Making predictions")
pred = model.predict(X)

# Calculate multiple metrics
mae = mean_absolute_error(y, pred)
mse = mean_squared_error(y, pred)
rmse = mse ** 0.5
r2 = r2_score(y, pred)

logger.info("Logging metrics")
# Log to MLflow
mlflow.log_metric("mae_test", mae)
mlflow.log_metric("mse_test", mse)
mlflow.log_metric("rmse_test", rmse)
mlflow.log_metric("r2_test", r2)

# Log to W&B (if initialized)
try:
    wandb.log({
        "test/mae": mae,
        "test/mse": mse,
        "test/rmse": rmse,
        "test/r2": r2,
        "test_metric": mae  # For the simple metric visualization
    })
    
    # Log test results as a summary
    wandb.summary.update({
        "test_mae": mae,
        "test_mse": mse,
        "test_rmse": rmse,
        "test_r2": r2
    })
except wandb.errors.Error:
    # W&B not initialized, skip logging
    logger.info("W&B not initialized, skipping W&B logging")

logger.info(f"Test MAE = {mae:.3f}, RMSE = {rmse:.3f}, R² = {r2:.3f}")
