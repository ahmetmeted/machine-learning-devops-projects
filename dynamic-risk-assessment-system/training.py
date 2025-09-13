import pandas as pd
import numpy as np
import json
import pickle
import os
import logging
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_model():
    """
    Function for training the model
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    output_folder_path = config['output_folder_path']
    output_model_path = config['output_model_path']
    
    # Read finaldata.csv
    final_data_path = os.path.join(output_folder_path, 'finaldata.csv')
    if not os.path.exists(final_data_path):
        logger.error(f"Final data file not found at {final_data_path}")
        return
    
    df = pd.read_csv(final_data_path)
    logger.info(f"Loaded training data with shape: {df.shape}")
    
    # Prepare features and target
    # Exclude 'corporation' column and use the rest as features
    feature_columns = [col for col in df.columns if col not in ['corporation', 'exited']]
    X = df[feature_columns]
    y = df['exited']
    
    logger.info(f"Feature columns: {feature_columns}")
    logger.info(f"Target distribution: {y.value_counts().to_dict()}")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train logistic regression model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)
    
    # Make predictions on test set
    y_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_pred)
    
    logger.info(f"Model trained successfully. F1 score: {f1:.4f}")
    
    # Save the model
    os.makedirs(output_model_path, exist_ok=True)
    model_path = os.path.join(output_model_path, 'trainedmodel.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    logger.info(f"Model saved to {model_path}")
    
    return model

if __name__ == '__main__':
    train_model()

