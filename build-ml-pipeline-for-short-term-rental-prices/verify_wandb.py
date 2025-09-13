#!/usr/bin/env python3
"""
Script to verify W&B integration and project accessibility.
"""
import os
import wandb
from omegaconf import OmegaConf

def verify_wandb_setup():
    """Verify W&B setup and project accessibility."""
    print("🔍 Verifying W&B setup...")
    
    # Load config
    cfg = OmegaConf.load("config.yaml")
    
    # Set API key
    os.environ["WANDB_API_KEY"] = cfg["wandb"]["api_key"]
    
    try:
        # Initialize W&B
        run = wandb.init(
            project=cfg["wandb"]["project"],
            entity=cfg["wandb"]["entity"],
            name="verification_run",
            tags=["verification"],
            config={
                "verification": True,
                "project": cfg["wandb"]["project"],
                "entity": cfg["wandb"]["entity"]
            }
        )
        
        print(f"✅ W&B initialized successfully!")
        print(f"📊 Project: {cfg['wandb']['project']}")
        print(f"👤 Entity: {cfg['wandb']['entity']}")
        print(f"🔗 Run URL: {run.url}")
        
        # Log a test metric
        wandb.log({"test_metric": 1.0})
        
        # Finish the run
        wandb.finish()
        
        print("✅ W&B verification completed successfully!")
        print(f"🌐 View your project at: https://wandb.ai/{cfg['wandb']['entity']}/{cfg['wandb']['project']}")
        
        return True
        
    except Exception as e:
        print(f"❌ W&B verification failed: {e}")
        return False

if __name__ == "__main__":
    verify_wandb_setup()
