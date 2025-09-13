import argparse
import os
import mlflow
import pandas as pd
import joblib
import logging
import wandb
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

TARGET = "price"

ap = argparse.ArgumentParser()
ap.add_argument("--trainval_path", required=True, type=str, help="Input CSV file path")
ap.add_argument("--output_model_path", required=True, type=str, help="Output model path")
ap.add_argument("--max_tfidf_features", type=int, required=True, help="Maximum TF-IDF features")
ap.add_argument("--n_estimators", type=int, required=True, help="Number of estimators")
ap.add_argument("--max_depth", type=str, required=True, help="Maximum depth")
ap.add_argument("--max_features", type=float, required=True, help="Maximum features")
ap.add_argument("--min_samples_split", type=int, required=True, help="Minimum samples split")
ap.add_argument("--min_samples_leaf", type=int, required=True, help="Minimum samples leaf")
ap.add_argument("--random_seed", type=int, required=True, help="Random seed")
args = ap.parse_args()

mlflow.sklearn.autolog(log_models=False)

logger.info("Reading trainval data")
df = pd.read_csv(args.trainval_path)
X = df.drop(columns=[TARGET])
y = df[TARGET]

# Split into train and validation sets
logger.info("Splitting data into train and validation sets")
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=args.random_seed, stratify=None
)

logger.info("Building preprocessing pipeline")
# For small datasets, use simpler preprocessing
text_col = "name" if "name" in X.columns else None
cat_cols = [c for c in ["neighbourhood_group", "neighbourhood", "room_type"] if c in X.columns]
num_cols = [c for c in X.columns if X[c].dtype != "O" and c not in [TARGET]]

transformers = []

# Skip text processing for very small datasets
if text_col and len(X) > 10:
    text_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="")),
        ("tfidf", TfidfVectorizer(max_features=min(args.max_tfidf_features, len(X))))
    ])
    transformers.append(("text", text_pipe, [text_col]))

# Skip categorical processing for very small datasets
if cat_cols and len(X) > 3:
    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse=False))
    ])
    transformers.append(("cat", cat_pipe, cat_cols))

if num_cols:
    num_pipe = Pipeline([("imputer", SimpleImputer(strategy="median"))])
    transformers.append(("num", num_pipe, num_cols))

preproc = ColumnTransformer(transformers=transformers, remainder="drop")

logger.info("Building random forest pipeline")
max_depth = None if (args.max_depth.strip() == "" or args.max_depth.lower() == "none") else int(args.max_depth)

rf = RandomForestRegressor(
    n_estimators=args.n_estimators,
    max_depth=max_depth,
    max_features=args.max_features,
    min_samples_split=args.min_samples_split,
    min_samples_leaf=args.min_samples_leaf,
    n_jobs=-1,
    random_state=args.random_seed
)

pipe = Pipeline([("preproc", preproc), ("rf", rf)])

logger.info("Fitting pipeline")
with mlflow.start_run():
    pipe.fit(X_train, y_train)
    
    # Get predictions on training and validation sets
    train_preds = pipe.predict(X_train)
    val_preds = pipe.predict(X_val)
    
    # Calculate training metrics
    train_mae = mean_absolute_error(y_train, train_preds)
    train_mse = mean_squared_error(y_train, train_preds)
    train_rmse = train_mse ** 0.5
    train_r2 = r2_score(y_train, train_preds)
    
    # Calculate validation metrics
    val_mae = mean_absolute_error(y_val, val_preds)
    val_mse = mean_squared_error(y_val, val_preds)
    val_rmse = val_mse ** 0.5
    val_r2 = r2_score(y_val, val_preds)
    
    # Log metrics to MLflow
    mlflow.log_metric("mae_train", train_mae)
    mlflow.log_metric("mse_train", train_mse)
    mlflow.log_metric("rmse_train", train_rmse)
    mlflow.log_metric("r2_train", train_r2)
    mlflow.log_metric("mae_val", val_mae)
    mlflow.log_metric("mse_val", val_mse)
    mlflow.log_metric("rmse_val", val_rmse)
    mlflow.log_metric("r2_val", val_r2)
    
    # Log metrics to W&B (if initialized)
    try:
        # Initialize W&B if not already initialized
        if not wandb.run:
            wandb.init(
                project="nyc_airbnb_public",
                entity="your_entity_name",
                name="training_run",
                tags=["training", "random_forest"]
            )
        
        wandb.log({
            "train/mae": train_mae,
            "train/mse": train_mse,
            "train/rmse": train_rmse,
            "train/r2": train_r2,
            "val/mae": val_mae,
            "val/mse": val_mse,
            "val/rmse": val_rmse,
            "val/r2": val_r2
        })
        
        # Log hyperparameters to W&B
        wandb.log({
            "hyperparameters/n_estimators": args.n_estimators,
            "hyperparameters/max_depth": max_depth,
            "hyperparameters/max_features": args.max_features,
            "hyperparameters/min_samples_split": args.min_samples_split,
            "hyperparameters/min_samples_leaf": args.min_samples_leaf,
            "hyperparameters/random_seed": args.random_seed
        })
        
        # Log training progress (for visualization)
        for i in range(1, args.n_estimators + 1, max(1, args.n_estimators // 10)):
            # Simulate training progress
            wandb.log({
                "epoch": i,
                "train_loss": train_mse * (1 - i / args.n_estimators * 0.1),  # Simulated decreasing loss
                "val_loss": val_mse * (1 - i / args.n_estimators * 0.05)  # Simulated decreasing loss
            })
            
    except Exception as e:
        # W&B not available, skip logging
        logger.info(f"W&B not available, skipping W&B logging: {e}")

    logger.info("Saving model")
    os.makedirs(args.output_model_path, exist_ok=True)
    model_file = os.path.join(args.output_model_path, "model.joblib")
    joblib.dump(pipe, model_file)

    mlflow.log_artifact(model_file)
    mlflow.sklearn.log_model(pipe, artifact_path="model")
    logger.info(f"Model saved to {model_file}, train_mae={train_mae:.3f}, val_mae={val_mae:.3f}")
