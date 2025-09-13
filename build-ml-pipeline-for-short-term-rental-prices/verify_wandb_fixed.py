#!/usr/bin/env python3
"""
Verification script to test W&B integration with proper metrics
"""

import os
import sys
import wandb
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

def test_wandb_metrics():
    """Test W&B logging with proper metrics"""
    
    # Initialize W&B
    wandb.init(
        project="nyc_airbnb_public",
        entity="your_entity_name",
        name="verification_run",
        tags=["verification", "metrics_test"]
    )
    
    # Create sample data
    np.random.seed(42)
    n_samples = 100
    X = np.random.randn(n_samples, 5)
    y = 2 * X[:, 0] + 3 * X[:, 1] + np.random.randn(n_samples) * 0.1
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestRegressor(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Get predictions
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    # Calculate metrics
    train_mae = mean_absolute_error(y_train, train_pred)
    train_mse = mean_squared_error(y_train, train_pred)
    train_r2 = r2_score(y_train, train_pred)
    
    test_mae = mean_absolute_error(y_test, test_pred)
    test_mse = mean_squared_error(y_test, test_pred)
    test_r2 = r2_score(y_test, test_pred)
    
    # Log metrics
    wandb.log({
        "train/mae": train_mae,
        "train/mse": train_mse,
        "train/r2": train_r2,
        "test/mae": test_mae,
        "test/mse": test_mse,
        "test/r2": test_r2,
        "test_metric": test_mae  # Simple metric for visualization
    })
    
    # Log hyperparameters
    wandb.log({
        "hyperparameters/n_estimators": 10,
        "hyperparameters/random_state": 42
    })
    
    # Log training progress simulation
    for i in range(1, 11):
        wandb.log({
            "epoch": i,
            "train_loss": train_mse * (1 - i / 10 * 0.1),
            "val_loss": test_mse * (1 - i / 10 * 0.05)
        })
    
    # Update summary
    wandb.summary.update({
        "final_train_mae": train_mae,
        "final_test_mae": test_mae,
        "final_test_r2": test_r2
    })
    
    print(f"Logged metrics - Train MAE: {train_mae:.3f}, Test MAE: {test_mae:.3f}")
    
    wandb.finish()

if __name__ == "__main__":
    test_wandb_metrics()
