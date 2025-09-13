#!/usr/bin/env python3
"""
Model selection script to find and tag the best performing model.
"""

import mlflow
import pandas as pd
import os
import shutil

def find_best_model():
    """Find the best model based on MAE metric."""
    print("🔍 Searching for the best model...")
    
    # Connect to MLflow
    client = mlflow.tracking.MlflowClient()
    
    # Get all experiments
    experiments = client.search_experiments()
    
    best_run = None
    best_mae = float('inf')
    
    for exp in experiments:
        if exp.name == "short_term_rental_pipeline":
            runs = client.search_runs(experiment_ids=[exp.experiment_id])
            
            for run in runs:
                if 'mae_train' in run.data.metrics:
                    mae = run.data.metrics['mae_train']
                    if mae < best_mae:
                        best_mae = mae
                        best_run = run
    
    if best_run:
        print(f"🏆 Best model found!")
        print(f"Run ID: {best_run.info.run_id}")
        print(f"MAE: {best_mae:.4f}")
        
        # Copy the best model to a production directory
        model_path = f"mlruns/{best_run.info.experiment_id}/{best_run.info.run_id}/artifacts/model"
        prod_path = "artifacts/best_model"
        
        if os.path.exists(model_path):
            os.makedirs(prod_path, exist_ok=True)
            shutil.copytree(model_path, f"{prod_path}/model", dirs_exist_ok=True)
            print(f"✅ Best model copied to {prod_path}")
            
            # Create a simple tag file
            with open(f"{prod_path}/model_info.txt", "w") as f:
                f.write(f"Best Model Information\n")
                f.write(f"Run ID: {best_run.info.run_id}\n")
                f.write(f"MAE: {best_mae:.4f}\n")
                f.write(f"Experiment: {best_run.info.experiment_id}\n")
            
            return best_run.info.run_id, best_mae
        else:
            print("❌ Model artifacts not found")
            return None, None
    else:
        print("❌ No suitable model found")
        return None, None

def main():
    """Main function to select and tag the best model."""
    print("🎯 Model Selection Process")
    print("=" * 40)
    
    run_id, mae = find_best_model()
    
    if run_id:
        print(f"\n✅ Best model selected and tagged!")
        print(f"Run ID: {run_id}")
        print(f"MAE: {mae:.4f}")
        print("\nTo use this model, run:")
        print("mlflow run . -P steps=test_regression_model --env-manager=local")
    else:
        print("\n❌ No suitable model found. Please run training first.")

if __name__ == "__main__":
    main()
