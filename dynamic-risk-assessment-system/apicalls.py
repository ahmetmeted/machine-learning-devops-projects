import requests
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def call_api_endpoints():
    """
    Function to call API endpoints and combine outputs
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    output_model_path = config['output_model_path']
    test_data_path = config['test_data_path']
    
    base_url = "http://localhost:8000"
    results = {}
    
    try:
        # Call prediction endpoint
        logger.info("Calling prediction endpoint...")
        prediction_data = {"filepath": os.path.join(test_data_path, "testdata.csv")}
        prediction_response = requests.post(f"{base_url}/prediction", json=prediction_data)
        
        if prediction_response.status_code == 200:
            results['predictions'] = prediction_response.json()
            logger.info("Prediction endpoint successful")
        else:
            logger.error(f"Prediction endpoint failed: {prediction_response.status_code}")
            results['predictions'] = {'error': f"HTTP {prediction_response.status_code}"}
        
        # Call scoring endpoint
        logger.info("Calling scoring endpoint...")
        scoring_response = requests.get(f"{base_url}/scoring")
        
        if scoring_response.status_code == 200:
            results['scoring'] = scoring_response.json()
            logger.info("Scoring endpoint successful")
        else:
            logger.error(f"Scoring endpoint failed: {scoring_response.status_code}")
            results['scoring'] = {'error': f"HTTP {scoring_response.status_code}"}
        
        # Call summary stats endpoint
        logger.info("Calling summary stats endpoint...")
        summary_response = requests.get(f"{base_url}/summarystats")
        
        if summary_response.status_code == 200:
            results['summary_stats'] = summary_response.json()
            logger.info("Summary stats endpoint successful")
        else:
            logger.error(f"Summary stats endpoint failed: {summary_response.status_code}")
            results['summary_stats'] = {'error': f"HTTP {summary_response.status_code}"}
        
        # Call diagnostics endpoint
        logger.info("Calling diagnostics endpoint...")
        diagnostics_response = requests.get(f"{base_url}/diagnostics")
        
        if diagnostics_response.status_code == 200:
            results['diagnostics'] = diagnostics_response.json()
            logger.info("Diagnostics endpoint successful")
        else:
            logger.error(f"Diagnostics endpoint failed: {diagnostics_response.status_code}")
            results['diagnostics'] = {'error': f"HTTP {diagnostics_response.status_code}"}
        
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to API. Make sure the Flask app is running.")
        results = {'error': 'API connection failed'}
    except Exception as e:
        logger.error(f"Error calling API endpoints: {str(e)}")
        results = {'error': str(e)}
    
    # Save combined results
    os.makedirs(output_model_path, exist_ok=True)
    results_path = os.path.join(output_model_path, 'apireturns.txt')
    
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"API results saved to {results_path}")
    
    return results

if __name__ == '__main__':
    call_api_endpoints()

