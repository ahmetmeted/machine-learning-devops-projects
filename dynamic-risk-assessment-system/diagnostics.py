import pandas as pd
import numpy as np
import json
import pickle
import os
import time
import subprocess
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def model_predictions(dataframe):
    """
    Function to get model predictions
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    prod_deployment_path = config['prod_deployment_path']
    
    # Load deployed model
    model_path = os.path.join(prod_deployment_path, 'trainedmodel.pkl')
    if not os.path.exists(model_path):
        logger.error(f"Deployed model not found at {model_path}")
        return []
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    # Prepare features (exclude 'corporation' and 'exited' columns)
    feature_columns = [col for col in dataframe.columns if col not in ['corporation', 'exited']]
    X = dataframe[feature_columns]
    
    # Make predictions
    predictions = model.predict(X)
    
    return predictions.tolist()

def dataframe_summary():
    """
    Function to get summary statistics
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    output_folder_path = config['output_folder_path']
    
    # Read finaldata.csv
    final_data_path = os.path.join(output_folder_path, 'finaldata.csv')
    if not os.path.exists(final_data_path):
        logger.error(f"Final data file not found at {final_data_path}")
        return []
    
    df = pd.read_csv(final_data_path)
    
    # Calculate summary statistics for numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    summary_stats = []
    
    for col in numeric_columns:
        if col != 'exited':  # Exclude target variable
            stats = {
                'column': col,
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std()
            }
            summary_stats.append(stats)
    
    return summary_stats

def missing_data():
    """
    Function to check for missing data
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    output_folder_path = config['output_folder_path']
    
    # Read finaldata.csv
    final_data_path = os.path.join(output_folder_path, 'finaldata.csv')
    if not os.path.exists(final_data_path):
        logger.error(f"Final data file not found at {final_data_path}")
        return []
    
    df = pd.read_csv(final_data_path)
    
    # Calculate percentage of missing values for each column
    missing_percentages = []
    for col in df.columns:
        missing_pct = (df[col].isna().sum() / len(df)) * 100
        missing_percentages.append(missing_pct)
    
    return missing_percentages

def execution_time():
    """
    Function to get timing statistics
    """
    # Time data ingestion
    start_time = time.time()
    os.system('python ingestion.py')
    ingestion_time = time.time() - start_time
    
    # Time model training
    start_time = time.time()
    os.system('python training.py')
    training_time = time.time() - start_time
    
    return [ingestion_time, training_time]

def outdated_packages_list():
    """
    Function to check dependencies
    """
    # Read requirements.txt
    with open('requirements.txt', 'r') as f:
        requirements = f.read().strip().split('\n')
    
    outdated_packages = []
    
    for requirement in requirements:
        if '==' in requirement:
            package_name = requirement.split('==')[0]
            current_version = requirement.split('==')[1]
            
            try:
                # Get latest version using pip
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'index', 'versions', package_name],
                    capture_output=True, text=True, timeout=30
                )
                
                if result.returncode == 0:
                    # Parse the output to get latest version
                    output_lines = result.stdout.strip().split('\n')
                    latest_version = current_version  # Default to current if parsing fails
                    
                    for line in output_lines:
                        if 'Available versions:' in line:
                            versions = line.split('Available versions:')[1].strip()
                            if versions:
                                # Get the latest version (first one listed)
                                latest_version = versions.split(',')[0].strip()
                            break
                    
                    outdated_packages.append({
                        'package': package_name,
                        'current_version': current_version,
                        'latest_version': latest_version
                    })
                else:
                    # Fallback: use pip show
                    result = subprocess.run(
                        [sys.executable, '-m', 'pip', 'show', package_name],
                        capture_output=True, text=True, timeout=30
                    )
                    
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        for line in lines:
                            if line.startswith('Version:'):
                                latest_version = line.split('Version:')[1].strip()
                                break
                        
                        outdated_packages.append({
                            'package': package_name,
                            'current_version': current_version,
                            'latest_version': latest_version
                        })
                    else:
                        outdated_packages.append({
                            'package': package_name,
                            'current_version': current_version,
                            'latest_version': 'Unknown'
                        })
                        
            except Exception as e:
                logger.warning(f"Could not check version for {package_name}: {str(e)}")
                outdated_packages.append({
                    'package': package_name,
                    'current_version': current_version,
                    'latest_version': 'Unknown'
                })
    
    return outdated_packages

if __name__ == '__main__':
    # Test the functions
    print("Testing diagnostics functions...")
    
    # Test dataframe_summary
    summary = dataframe_summary()
    print(f"Summary statistics: {summary}")
    
    # Test missing_data
    missing = missing_data()
    print(f"Missing data percentages: {missing}")
    
    # Test execution_time
    timing = execution_time()
    print(f"Execution times: {timing}")
    
    # Test outdated_packages_list
    packages = outdated_packages_list()
    print(f"Package versions: {packages}")

