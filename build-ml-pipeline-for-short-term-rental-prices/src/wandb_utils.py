"""
W&B utilities for the NYC Airbnb price prediction pipeline.
"""
import os
import wandb
from omegaconf import DictConfig
from typing import Optional


def init_wandb(cfg: DictConfig, run_name: Optional[str] = None) -> wandb.run:
    """
    Initialize W&B run with configuration.
    
    Args:
        cfg: Hydra configuration object
        run_name: Optional custom run name
        
    Returns:
        wandb.run: Initialized W&B run object
    """
    # Set API key from config
    os.environ["WANDB_API_KEY"] = cfg["wandb"]["api_key"]
    
    # Convert config to a simple dictionary for W&B
    config_dict = {
        "project_name": cfg["main"]["project_name"],
        "experiment_name": cfg["main"]["experiment_name"],
        "min_price": cfg["etl"]["min_price"],
        "max_price": cfg["etl"]["max_price"],
        "test_size": cfg["modeling"]["test_size"],
        "random_seed": cfg["modeling"]["random_seed"],
        "max_tfidf_features": cfg["modeling"]["max_tfidf_features"],
        "n_estimators": cfg["modeling"]["random_forest"]["n_estimators"],
        "max_depth": cfg["modeling"]["random_forest"]["max_depth"],
        "max_features": cfg["modeling"]["random_forest"]["max_features"],
        "min_samples_split": cfg["modeling"]["random_forest"]["min_samples_split"],
        "min_samples_leaf": cfg["modeling"]["random_forest"]["min_samples_leaf"]
    }
    
    # Initialize W&B run with public project settings
    run = wandb.init(
        project=cfg["wandb"]["project"],
        entity=cfg["wandb"]["entity"],
        name=run_name,
        tags=cfg["wandb"]["tags"],
        config=config_dict,
        resume="allow",
        # Ensure the project is public
        settings=wandb.Settings(console="off")
    )
    
    return run


def log_artifact(file_path: str, artifact_name: str, artifact_type: str = "dataset"):
    """
    Log an artifact to W&B.
    
    Args:
        file_path: Path to the file to log
        artifact_name: Name for the artifact
        artifact_type: Type of artifact (dataset, model, etc.)
    """
    artifact = wandb.Artifact(
        name=artifact_name,
        type=artifact_type,
        description=f"Artifact from NYC Airbnb pipeline: {artifact_name}"
    )
    artifact.add_file(file_path)
    wandb.log_artifact(artifact)


def log_model_metrics(metrics: dict, prefix: str = ""):
    """
    Log model metrics to W&B.
    
    Args:
        metrics: Dictionary of metrics to log
        prefix: Optional prefix for metric names
    """
    if prefix:
        metrics = {f"{prefix}_{k}": v for k, v in metrics.items()}
    
    wandb.log(metrics)


def log_dataframe_table(df, table_name: str, max_rows: int = 1000):
    """
    Log a pandas DataFrame as a W&B table.
    
    Args:
        df: Pandas DataFrame to log
        table_name: Name for the table
        max_rows: Maximum number of rows to log
    """
    table = wandb.Table(dataframe=df.head(max_rows))
    wandb.log({table_name: table})
