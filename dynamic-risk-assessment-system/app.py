import pandas as pd
import json
import os
import logging
from flask import Flask, request, jsonify
from diagnostics import model_predictions, dataframe_summary, missing_data, execution_time, outdated_packages_list
import scoring

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/prediction", methods=['POST', 'OPTIONS'])
def predict():
    """
    Prediction endpoint
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Get file path from request
        data = request.get_json()
        if not data or 'filepath' not in data:
            return jsonify({'error': 'No filepath provided'}), 400
        
        filepath = data['filepath']
        
        # Check if file exists
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        # Read data
        df = pd.read_csv(filepath)
        
        # Get predictions
        predictions = model_predictions(df)
        
        return jsonify({'predictions': predictions}), 200
        
    except Exception as e:
        logger.error(f"Error in prediction endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route("/scoring", methods=['GET', 'OPTIONS'])
def score():
    """
    Scoring endpoint
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Run scoring script
        f1_score = scoring.score_model()
        
        return jsonify({'f1_score': f1_score}), 200
        
    except Exception as e:
        logger.error(f"Error in scoring endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route("/summarystats", methods=['GET', 'OPTIONS'])
def summary_stats():
    """
    Summary statistics endpoint
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Get summary statistics
        summary = dataframe_summary()
        
        return jsonify({'summary_statistics': summary}), 200
        
    except Exception as e:
        logger.error(f"Error in summary stats endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route("/diagnostics", methods=['GET', 'OPTIONS'])
def diagnostics():
    """
    Diagnostics endpoint
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Get diagnostics
        missing = missing_data()
        timing = execution_time()
        packages = outdated_packages_list()
        
        diagnostics_data = {
            'missing_data_percentages': missing,
            'execution_times': timing,
            'package_versions': packages
        }
        
        return jsonify(diagnostics_data), 200
        
    except Exception as e:
        logger.error(f"Error in diagnostics endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

