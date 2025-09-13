import os
import json
import subprocess
import logging
import time
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_for_new_data():
    """
    Check if there is new data to ingest
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    input_folder_path = config['input_folder_path']
    prod_deployment_path = config['prod_deployment_path']
    
    # Read list of previously ingested files
    ingested_files_path = os.path.join(prod_deployment_path, 'ingestedfiles.txt')
    previously_ingested = set()
    
    if os.path.exists(ingested_files_path):
        with open(ingested_files_path, 'r') as f:
            previously_ingested = set(line.strip() for line in f.readlines())
    
    # Check current files in input folder
    current_files = set()
    if os.path.exists(input_folder_path):
        current_files = set(f for f in os.listdir(input_folder_path) if f.endswith('.csv'))
    
    # Find new files
    new_files = current_files - previously_ingested
    
    logger.info(f"Previously ingested files: {previously_ingested}")
    logger.info(f"Current files: {current_files}")
    logger.info(f"New files: {new_files}")
    
    return len(new_files) > 0

def check_model_drift():
    """
    Check if model drift has occurred
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    prod_deployment_path = config['prod_deployment_path']
    
    # Read current model score
    current_score_path = os.path.join(prod_deployment_path, 'latestscore.txt')
    if not os.path.exists(current_score_path):
        logger.warning("No current model score found")
        return True  # Assume drift if no score
    
    with open(current_score_path, 'r') as f:
        current_score = float(f.read().strip())
    
    # Run scoring on new data
    logger.info("Running scoring on new data...")
    result = subprocess.run(['python', 'scoring.py'], capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"Scoring failed: {result.stderr}")
        return True  # Assume drift if scoring fails
    
    # Read new score
    output_model_path = config['output_model_path']
    new_score_path = os.path.join(output_model_path, 'latestscore.txt')
    
    if not os.path.exists(new_score_path):
        logger.warning("No new model score found")
        return True  # Assume drift if no new score
    
    with open(new_score_path, 'r') as f:
        new_score = float(f.read().strip())
    
    logger.info(f"Current score: {current_score}, New score: {new_score}")
    
    # Check for drift (new score is lower)
    drift_detected = new_score < current_score
    logger.info(f"Model drift detected: {drift_detected}")
    
    return drift_detected

def run_ingestion():
    """
    Run data ingestion
    """
    logger.info("Running data ingestion...")
    result = subprocess.run(['python', 'ingestion.py'], capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"Ingestion failed: {result.stderr}")
        return False
    
    logger.info("Data ingestion completed successfully")
    return True

def run_training():
    """
    Run model training
    """
    logger.info("Running model training...")
    result = subprocess.run(['python', 'training.py'], capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"Training failed: {result.stderr}")
        return False
    
    logger.info("Model training completed successfully")
    return True

def run_deployment():
    """
    Run model deployment
    """
    logger.info("Running model deployment...")
    result = subprocess.run(['python', 'deployment.py'], capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"Deployment failed: {result.stderr}")
        return False
    
    logger.info("Model deployment completed successfully")
    return True

def run_diagnostics_and_reporting():
    """
    Run diagnostics and reporting
    """
    logger.info("Running diagnostics and reporting...")
    
    # Run reporting
    result = subprocess.run(['python', 'reporting.py'], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Reporting failed: {result.stderr}")
        return False
    
    # Run API calls
    result = subprocess.run(['python', 'apicalls.py'], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"API calls failed: {result.stderr}")
        return False
    
    logger.info("Diagnostics and reporting completed successfully")
    return True

def main():
    """
    Main function to run the full process
    """
    logger.info("Starting full process automation...")
    start_time = time.time()
    
    # Step 1: Check for new data
    logger.info("Step 1: Checking for new data...")
    has_new_data = check_for_new_data()
    
    if not has_new_data:
        logger.info("No new data found. Exiting process.")
        return
    
    # Step 2: Ingest new data
    logger.info("Step 2: Ingesting new data...")
    if not run_ingestion():
        logger.error("Data ingestion failed. Exiting process.")
        return
    
    # Step 3: Check for model drift
    logger.info("Step 3: Checking for model drift...")
    drift_detected = check_model_drift()
    
    if not drift_detected:
        logger.info("No model drift detected. Current model is still good.")
        return
    
    # Step 4: Re-train model
    logger.info("Step 4: Re-training model...")
    if not run_training():
        logger.error("Model training failed. Exiting process.")
        return
    
    # Step 5: Re-deploy model
    logger.info("Step 5: Re-deploying model...")
    if not run_deployment():
        logger.error("Model deployment failed. Exiting process.")
        return
    
    # Step 6: Run diagnostics and reporting
    logger.info("Step 6: Running diagnostics and reporting...")
    if not run_diagnostics_and_reporting():
        logger.error("Diagnostics and reporting failed.")
        return
    
    end_time = time.time()
    total_time = end_time - start_time
    
    logger.info(f"Full process completed successfully in {total_time:.2f} seconds")

if __name__ == '__main__':
    main()

