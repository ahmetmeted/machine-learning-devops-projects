"""
Machine Learning Model for Census Income Prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os
from typing import Dict, Tuple


class CensusModel:
    """
    A machine learning model for predicting income based on census data.
    """

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoders = {}
        self.feature_columns = []
        self.target_column = 'income'
        self.is_trained = False

    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load and preprocess the census data.

        Args:
            filepath (str): Path to the CSV file

        Returns:
            pd.DataFrame: Preprocessed dataframe
        """
        # Define column names based on UCI Adult dataset
        columns = [
            'age', 'workclass', 'fnlgt', 'education', 'education-num',
            'marital-status', 'occupation', 'relationship', 'race', 'sex',
            'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'
        ]

        # Load data
        df = pd.read_csv(filepath, header=None, names=columns)

        # Remove any rows with missing values (represented as '?')
        df = df.replace('?', np.nan)
        df = df.dropna()

        # Clean up whitespace
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip()

        return df

    def preprocess_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Preprocess the data for training.

        Args:
            df (pd.DataFrame): Raw dataframe

        Returns:
            Tuple[pd.DataFrame, pd.Series]: Features and target
        """
        # Separate features and target
        X = df.drop('income', axis=1)
        y = df['income']

        # Store feature columns
        self.feature_columns = X.columns.tolist()

        # Encode categorical variables
        categorical_columns = X.select_dtypes(include=['object']).columns

        for col in categorical_columns:
            le = LabelEncoder()
            X.loc[:, col] = le.fit_transform(X[col])
            self.label_encoders[col] = le

        # Ensure all columns are numeric
        for col in X.columns:
            if X[col].dtype == 'object':
                le = LabelEncoder()
                X.loc[:, col] = le.fit_transform(X[col])
                self.label_encoders[col] = le

        # Encode target variable
        le_target = LabelEncoder()
        y = le_target.fit_transform(y)
        self.label_encoders[self.target_column] = le_target

        return X, y

    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """
        Train the model.

        Args:
            X (pd.DataFrame): Training features
            y (pd.Series): Training target

        Returns:
            Dict[str, float]: Training metrics
        """
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Train the model
        self.model.fit(X_train, y_train)

        # Make predictions
        y_pred = self.model.predict(X_test)

        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1': f1_score(y_test, y_pred, average='weighted')
        }

        self.is_trained = True
        return metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions on new data.

        Args:
            X (pd.DataFrame): Features for prediction

        Returns:
            np.ndarray: Predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")

        # Ensure we have the same columns as training data
        X = X[self.feature_columns].copy()

        # Encode categorical variables
        for col in X.select_dtypes(include=['object']).columns:
            if col in self.label_encoders:
                # Handle unseen labels by using the most common class
                try:
                    X.loc[:, col] = self.label_encoders[col].transform(X[col])
                except ValueError as e:
                    if "previously unseen labels" in str(e):
                        # For unseen labels, use the most common class (0)
                        X.loc[:, col] = 0
                    else:
                        raise e

        return self.model.predict(X)

    def save_model(self, model_path: str, encoder_path: str):
        """
        Save the trained model and encoders.

        Args:
            model_path (str): Path to save the model
            encoder_path (str): Path to save the encoders
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        os.makedirs(os.path.dirname(encoder_path), exist_ok=True)

        # Save model and encoders
        joblib.dump(self.model, model_path)
        joblib.dump(self.label_encoders, encoder_path)

    def load_model(self, model_path: str, encoder_path: str):
        """
        Load a trained model and encoders.

        Args:
            model_path (str): Path to the model file
            encoder_path (str): Path to the encoder file
        """
        self.model = joblib.load(model_path)
        self.label_encoders = joblib.load(encoder_path)

        # Set feature columns from the loaded model
        if hasattr(self.model, 'feature_names_in_'):
            self.feature_columns = list(self.model.feature_names_in_)
        else:
            # Fallback to encoder keys
            self.feature_columns = [col for col in self.label_encoders.keys() if col != self.target_column]

        self.is_trained = True

    def get_slice_performance(self, df: pd.DataFrame, feature: str) -> Dict[str, Dict[str, float]]:
        """
        Calculate model performance on slices of data for a given categorical feature.

        Args:
            df (pd.DataFrame): Full dataset
            feature (str): Feature to slice on

        Returns:
            Dict[str, Dict[str, float]]: Performance metrics for each slice
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before calculating slice performance")

        # Preprocess the data
        X, y = self.preprocess_data(df)

        # Get unique values for the feature
        unique_values = df[feature].unique()
        slice_performance = {}

        for value in unique_values:
            # Create slice
            mask = df[feature] == value
            X_slice = X[mask]
            y_slice = y[mask]

            if len(X_slice) == 0:
                continue

            # Make predictions using the preprocessed data
            y_pred = self.model.predict(X_slice)

            # Calculate metrics
            slice_performance[value] = {
                'accuracy': accuracy_score(y_slice, y_pred),
                'precision': precision_score(y_slice, y_pred, average='weighted', zero_division=0),
                'recall': recall_score(y_slice, y_pred, average='weighted', zero_division=0),
                'f1': f1_score(y_slice, y_pred, average='weighted', zero_division=0),
                'count': len(X_slice)
            }

        return slice_performance


def train_model():
    """
    Train the model and save it.
    """
    # Initialize model
    model = CensusModel()

    # Load and preprocess data
    print("Loading data...")
    df = model.load_data('census.csv')
    print(f"Data loaded: {df.shape}")

    print("Preprocessing data...")
    X, y = model.preprocess_data(df)
    print(f"Features shape: {X.shape}, Target shape: {y.shape}")

    # Train model
    print("Training model...")
    metrics = model.train(X, y)
    print("Training metrics:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")

    # Save model
    print("Saving model...")
    model.save_model('model/model.pkl', 'model/encoders.pkl')
    print("Model saved successfully!")

    return model, df


if __name__ == "__main__":
    model, df = train_model()
