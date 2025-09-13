import pandas as pd
import numpy as np
import json
import pickle
import os
import logging
from sklearn.metrics import f1_score

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def score_model():
    """
    Function for scoring the model
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    test_data_path = config['test_data_path']
    output_model_path = config['output_model_path']
    
    # Read test data
    test_data_file = os.path.join(test_data_path, 'testdata.csv')
    if not os.path.exists(test_data_file):
        logger.error(f"Test data file not found at {test_data_file}")
        return
    
    df = pd.read_csv(test_data_file)
    logger.info(f"Loaded test data with shape: {df.shape}")
    
    # Load trained model
    model_path = os.path.join(output_model_path, 'trainedmodel.pkl')
    if not os.path.exists(model_path):
        logger.error(f"Trained model not found at {model_path}")
        return
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    # Prepare features and target
    feature_columns = [col for col in df.columns if col not in ['corporation', 'exited']]
    X = df[feature_columns]
    y = df['exited']
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Calculate F1 score
    f1 = f1_score(y, y_pred)
    
    logger.info(f"F1 score on test data: {f1:.4f}")
    
    # Save F1 score
    score_path = os.path.join(output_model_path, 'latestscore.txt')
    with open(score_path, 'w') as f:
        f.write(str(f1))
    
    logger.info(f"F1 score saved to {score_path}")
    
    return f1

if __name__ == '__main__':
    score_model()

