#!/usr/bin/env python3
"""
Hyperparameter optimization script for the ML pipeline.
This script runs multiple experiments with different hyperparameters.
"""

import subprocess
import os
import sys

def run_experiment(max_tfidf_features, max_features, n_estimators, max_depth):
    """Run a single experiment with given hyperparameters."""
    print(f"Running experiment: max_tfidf_features={max_tfidf_features}, max_features={max_features}, n_estimators={n_estimators}, max_depth={max_depth}")
    
    cmd = [
        "mlflow", "run", ".",
        "-P", f"hydra_options=modeling.max_tfidf_features={max_tfidf_features} modeling.random_forest.max_features={max_features} modeling.random_forest.n_estimators={n_estimators} modeling.random_forest.max_depth={max_depth}",
        "--env-manager=local"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ Experiment completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Experiment failed: {e}")
        return False

def main():
    """Run hyperparameter optimization experiments."""
    print("🚀 Starting Hyperparameter Optimization")
    print("=" * 50)
    
    # Define hyperparameter search space
    max_tfidf_features_list = [10, 15, 30]
    max_features_list = [0.1, 0.33, 0.5, 0.75, 1.0]
    n_estimators_list = [100, 200, 300]
    max_depth_list = [10, 20, None]
    
    successful_experiments = 0
    total_experiments = 0
    
    for max_tfidf in max_tfidf_features_list:
        for max_feat in max_features_list:
            for n_est in n_estimators_list:
                for max_dep in max_depth_list:
                    total_experiments += 1
                    max_depth_str = "null" if max_dep is None else str(max_dep)
                    
                    if run_experiment(max_tfidf, max_feat, n_est, max_depth_str):
                        successful_experiments += 1
                    
                    print("-" * 30)
    
    print("=" * 50)
    print(f"🎯 Optimization Complete!")
    print(f"Successful experiments: {successful_experiments}/{total_experiments}")
    print("Check MLflow UI to compare results and select the best model.")

if __name__ == "__main__":
    main()
