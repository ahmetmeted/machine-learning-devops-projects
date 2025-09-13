#!/usr/bin/env python3
"""
Fix W&B metrics with correct values
"""

import pandas as pd
import joblib
import os
import wandb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def log_correct_metrics():
    """Log correct metrics to W&B"""
    
    # Initialize W&B
    wandb.init(
        project="nyc_airbnb_public",
        entity="your_entity_name",
        name="corrected_metrics",
        tags=["corrected", "real_metrics"]
    )
    
    # Load model and data
    model_path = 'artifacts/random_forest_model/model.joblib'
    model = joblib.load(model_path)
    
    train_df = pd.read_csv('artifacts/trainval_data.csv')
    test_df = pd.read_csv('artifacts/test_data.csv')
    
    # Training metrics
    X_train = train_df.drop(columns=['price'])
    y_train = train_df['price']
    train_pred = model.predict(X_train)
    
    train_mae = mean_absolute_error(y_train, train_pred)
    train_mse = mean_squared_error(y_train, train_pred)
    train_rmse = train_mse ** 0.5
    train_r2 = r2_score(y_train, train_pred)
    
    # Test metrics
    X_test = test_df.drop(columns=['price'])
    y_test = test_df['price']
    test_pred = model.predict(X_test)
    
    test_mae = mean_absolute_error(y_test, test_pred)
    test_mse = mean_squared_error(y_test, test_pred)
    test_rmse = test_mse ** 0.5
    test_r2 = r2_score(y_test, test_pred)
    
    # Log correct metrics
    wandb.log({
        "train/mae": train_mae,
        "train/mse": train_mse,
        "train/rmse": train_rmse,
        "train/r2": train_r2,
        "test/mae": test_mae,
        "test/mse": test_mse,
        "test/rmse": test_rmse,
        "test/r2": test_r2,
        "test_metric": test_mae
    })
    
    # Log hyperparameters
    wandb.log({
        "hyperparameters/n_estimators": 200,
        "hyperparameters/max_depth": None,
        "hyperparameters/max_features": 0.5,
        "hyperparameters/min_samples_split": 2,
        "hyperparameters/min_samples_leaf": 1,
        "hyperparameters/random_seed": 42
    })
    
    # Log data info
    wandb.log({
        "data/train_samples": len(train_df),
        "data/test_samples": len(test_df),
        "data/price_min": train_df['price'].min(),
        "data/price_max": train_df['price'].max(),
        "data/price_mean": train_df['price'].mean()
    })
    
    print(f"Logged correct metrics:")
    print(f"Train MAE: {train_mae:.3f}, Test MAE: {test_mae:.3f}")
    print(f"Train R²: {train_r2:.3f}, Test R²: {test_r2:.3f}")
    
    wandb.finish()

if __name__ == "__main__":
    log_correct_metrics()
