import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def merge_multiple_dataframe():
    """
    Function for data ingestion
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    input_folder_path = config['input_folder_path']
    output_folder_path = config['output_folder_path']
    
    # Check for datasets, compile them together, and write to an output file
    logger.info("Starting data ingestion process")
    
    # Get list of all CSV files in input folder
    csv_files = [f for f in os.listdir(input_folder_path) if f.endswith('.csv')]
    logger.info(f"Found {len(csv_files)} CSV files: {csv_files}")
    
    # Read and combine all CSV files
    dataframes = []
    ingested_files = []
    
    for file in csv_files:
        file_path = os.path.join(input_folder_path, file)
        try:
            df = pd.read_csv(file_path)
            dataframes.append(df)
            ingested_files.append(file)
            logger.info(f"Successfully read {file} with {len(df)} rows")
        except Exception as e:
            logger.error(f"Error reading {file}: {str(e)}")
    
    if not dataframes:
        logger.error("No valid CSV files found to process")
        return
    
    # Combine all dataframes
    final_df = pd.concat(dataframes, ignore_index=True)
    logger.info(f"Combined dataset shape: {final_df.shape}")
    
    # Remove duplicates
    initial_rows = len(final_df)
    final_df = final_df.drop_duplicates()
    final_rows = len(final_df)
    logger.info(f"Removed {initial_rows - final_rows} duplicate rows")
    
    # Save final dataset
    os.makedirs(output_folder_path, exist_ok=True)
    final_data_path = os.path.join(output_folder_path, 'finaldata.csv')
    final_df.to_csv(final_data_path, index=False)
    logger.info(f"Final dataset saved to {final_data_path}")
    
    # Save record of ingested files
    ingested_files_path = os.path.join(output_folder_path, 'ingestedfiles.txt')
    with open(ingested_files_path, 'w') as f:
        for file in ingested_files:
            f.write(file + '\n')
    logger.info(f"Ingested files record saved to {ingested_files_path}")
    
    return final_df

if __name__ == '__main__':
    merge_multiple_dataframe()

