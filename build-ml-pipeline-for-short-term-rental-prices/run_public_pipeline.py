#!/usr/bin/env python3
"""
Script to run the ML pipeline with public W&B configuration.
This ensures all data and models are logged to the public project.
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    """Run the ML pipeline with public configuration."""
    
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    
    # Set environment variables for public configuration
    os.environ["WANDB_PROJECT"] = "nyc_airbnb_public"
    os.environ["WANDB_ENTITY"] = "your_entity_name"
    os.environ["WANDB_API_KEY"] = "your_wandb_api_key"
    
    print("🚀 Starting ML Pipeline with Public W&B Configuration")
    print("=" * 60)
    print(f"Project: nyc_airbnb_public")
    print(f"Entity: your_entity_name")
    print(f"API Key: {os.environ['WANDB_API_KEY'][:10]}...")
    print("=" * 60)
    
    # Run the main pipeline with public config
    try:
        # Change to project directory
        os.chdir(project_root)
        
        # Run the pipeline using the public configuration
        cmd = [
            sys.executable, "main.py",
            "--config-name", "config_public"
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        print()
        
        # Execute the pipeline
        result = subprocess.run(cmd, check=True, capture_output=False)
        
        print()
        print("✅ Pipeline completed successfully!")
        print("📊 Check your public W&B project at: https://wandb.ai/your_entity_name/nyc_airbnb_public")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Pipeline failed with error code: {e.returncode}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
