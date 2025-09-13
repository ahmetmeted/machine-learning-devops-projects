import os
import json
import mlflow
import hydra
import wandb
from omegaconf import DictConfig
import hydra.utils
from src.wandb_utils import init_wandb, log_artifact


@hydra.main(version_base=None, config_path=".", config_name="config")
def go(cfg: DictConfig):
    mlflow.set_experiment(cfg["main"]["experiment_name"])
    
    # Initialize W&B
    wandb_run = init_wandb(cfg, run_name=f"pipeline_run_{os.getenv('MLFLOW_RUN_ID', 'local')}")
    
    steps_param = os.getenv("STEPS", "download,basic_cleaning,data_check,train_val_test_split,train_random_forest,test_regression_model")
    active_steps = [s.strip() for s in steps_param.split(",") if s.strip()]
    project_root = hydra.utils.get_original_cwd()

    if "download" in active_steps:
        import subprocess
        subprocess.run([
            "python", os.path.join(project_root, "src", "get_data", "run.py"),
            "--input_filename", os.path.join(project_root, "data", "raw", cfg["etl"]["sample"]),
            "--output_path", os.path.join(project_root, "artifacts", "sample.csv")
        ], check=True)
        # Log raw data artifact
        log_artifact(
            os.path.join(project_root, "artifacts", "sample.csv"),
            "raw_sample_data",
            "dataset"
        )

    if "basic_cleaning" in active_steps:
        import subprocess
        subprocess.run([
            "python", os.path.join(project_root, "src", "basic_cleaning", "run.py"),
            "--input_path", os.path.join(project_root, "artifacts", "sample.csv"),
            "--output_path", os.path.join(project_root, "artifacts", "clean_sample.csv"),
            "--min_price", str(cfg['etl']['min_price']),
            "--max_price", str(cfg['etl']['max_price']),
            "--apply_geofence", "false",
            "--lon_min", str(cfg['etl']['geo_bounds']['lon_min']),
            "--lon_max", str(cfg['etl']['geo_bounds']['lon_max']),
            "--lat_min", str(cfg['etl']['geo_bounds']['lat_min']),
            "--lat_max", str(cfg['etl']['geo_bounds']['lat_max']),
        ], check=True)
        # Log cleaned data artifact
        log_artifact(
            os.path.join(project_root, "artifacts", "clean_sample.csv"),
            "cleaned_sample_data",
            "dataset"
        )

    if "data_check" in active_steps:
        import subprocess
        subprocess.run([
            "python", os.path.join(project_root, "src", "data_check", "run.py"),
            "--csv_path", os.path.join(project_root, "artifacts", "clean_sample.csv"),
            "--min_rows", str(cfg["data_check"]["min_rows"]),
            "--max_rows", str(cfg["data_check"]["max_rows"]),
            "--min_price", str(cfg["data_check"]["min_price"]),
            "--max_price", str(cfg["data_check"]["max_price"]),
        ], check=True)

    if "train_val_test_split" in active_steps:
        import subprocess
        subprocess.run([
            "python", os.path.join(project_root, "src", "train_val_test_split", "run.py"),
            "--input_path", os.path.join(project_root, "artifacts", "clean_sample.csv"),
            "--trainval_out", os.path.join(project_root, "artifacts", "trainval_data.csv"),
            "--test_out", os.path.join(project_root, "artifacts", "test_data.csv"),
            "--test_size", str(cfg["modeling"]["test_size"]),
            "--random_seed", str(cfg["modeling"]["random_seed"]),
            "--stratify_by", cfg["modeling"]["stratify_by"],
        ], check=True)
        # Log train/val and test data artifacts
        log_artifact(
            os.path.join(project_root, "artifacts", "trainval_data.csv"),
            "trainval_data",
            "dataset"
        )
        log_artifact(
            os.path.join(project_root, "artifacts", "test_data.csv"),
            "test_data",
            "dataset"
        )

    if "train_random_forest" in active_steps:
        import subprocess
        rf = cfg["modeling"]["random_forest"]
        subprocess.run([
            "python", os.path.join(project_root, "src", "train_random_forest", "run.py"),
            "--trainval_path", os.path.join(project_root, "artifacts", "trainval_data.csv"),
            "--output_model_path", os.path.join(project_root, "artifacts", "random_forest_model"),
            "--max_tfidf_features", str(cfg["modeling"]["max_tfidf_features"]),
            "--n_estimators", str(rf["n_estimators"]),
            "--max_depth", "" if rf["max_depth"] in [None, "null"] else str(rf["max_depth"]),
            "--max_features", str(rf["max_features"]),
            "--min_samples_split", str(rf["min_samples_split"]),
            "--min_samples_leaf", str(rf["min_samples_leaf"]),
            "--random_seed", str(cfg["modeling"]["random_seed"]),
        ], check=True)
        # Log trained model artifact
        log_artifact(
            os.path.join(project_root, "artifacts", "random_forest_model", "model.joblib"),
            "random_forest_model",
            "model"
        )

    if "test_regression_model" in active_steps:
        import subprocess
        subprocess.run([
            "python", os.path.join(project_root, "src", "test_regression_model", "run.py"),
            "--model_uri", os.path.join(project_root, "artifacts", "random_forest_model"),
            "--test_csv", os.path.join(project_root, "artifacts", "test_data.csv")
        ], check=True)
    
    # Finish W&B run
    wandb.finish()


if __name__ == "__main__":
    go()
