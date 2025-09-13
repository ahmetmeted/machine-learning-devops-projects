import shutil
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def store_model_into_pickle():
    """
    Function for deployment
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    output_model_path = config['output_model_path']
    output_folder_path = config['output_folder_path']
    prod_deployment_path = config['prod_deployment_path']
    
    # Create production deployment directory
    os.makedirs(prod_deployment_path, exist_ok=True)
    
    # Files to copy
    files_to_copy = [
        ('trainedmodel.pkl', output_model_path),
        ('latestscore.txt', output_model_path),
        ('ingestedfiles.txt', output_folder_path)
    ]
    
    # Copy files to production deployment
    for filename, source_dir in files_to_copy:
        source_path = os.path.join(source_dir, filename)
        dest_path = os.path.join(prod_deployment_path, filename)
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            logger.info(f"Copied {filename} to production deployment")
        else:
            logger.warning(f"File {filename} not found in {source_dir}")
    
    logger.info("Model deployment completed")

if __name__ == '__main__':
    store_model_into_pickle()

