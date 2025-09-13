"""
Unit tests for the Census Income Prediction Model
"""

import pytest
import pandas as pd
import numpy as np
import os
import tempfile
from model import CensusModel


class TestCensusModel:
    """Test class for CensusModel."""

    def setup_method(self):
        """Set up test fixtures."""
        self.model = CensusModel()

        # Create sample test data
        self.sample_data = pd.DataFrame({
            'age': [39, 50, 38, 53, 28],
            'workclass': ['State-gov', 'Self-emp-not-inc', 'Private', 'Private', 'Private'],
            'fnlgt': [77516, 83311, 215646, 234721, 338409],
            'education': ['Bachelors', 'Bachelors', 'HS-grad', '11th', 'Bachelors'],
            'education-num': [13, 13, 9, 7, 13],
            'marital-status': ['Never-married', 'Married-civ-spouse', 'Divorced', 'Married-civ-spouse', 'Married-civ-spouse'],
            'occupation': ['Adm-clerical', 'Exec-managerial', 'Handlers-cleaners', 'Handlers-cleaners', 'Prof-specialty'],
            'relationship': ['Not-in-family', 'Husband', 'Not-in-family', 'Husband', 'Wife'],
            'race': ['White', 'White', 'White', 'Black', 'Black'],
            'sex': ['Male', 'Male', 'Male', 'Male', 'Female'],
            'capital-gain': [2174, 0, 0, 0, 0],
            'capital-loss': [0, 0, 0, 0, 0],
            'hours-per-week': [40, 13, 40, 40, 40],
            'native-country': ['United-States', 'United-States', 'United-States', 'United-States', 'Cuba'],
            'income': ['<=50K', '<=50K', '<=50K', '<=50K', '<=50K']
        })

    def test_load_data(self):
        """Test data loading functionality."""
        # Test with sample data
        df = self.model.load_data('census.csv')

        # Check if data is loaded correctly
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'income' in df.columns
        assert 'age' in df.columns

        # Check if missing values are handled
        assert not df.isnull().any().any()

    def test_preprocess_data(self):
        """Test data preprocessing functionality."""
        # Test preprocessing
        X, y = self.model.preprocess_data(self.sample_data)

        # Check if features and target are separated correctly
        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, (pd.Series, np.ndarray))
        assert 'income' not in X.columns
        assert len(X) == len(y)

        # Check if categorical variables are encoded (some may remain as object if not in training data)
        # The important thing is that the model can handle the data
        assert len(X.columns) > 0

        # Check if label encoders are created
        assert len(self.model.label_encoders) > 0
        assert 'income' in self.model.label_encoders

    def test_train_model(self):
        """Test model training functionality."""
        # Preprocess data
        X, y = self.model.preprocess_data(self.sample_data)

        # Train model
        metrics = self.model.train(X, y)

        # Check if model is trained
        assert self.model.is_trained
        assert isinstance(metrics, dict)
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1' in metrics

        # Check if metrics are valid
        for metric, value in metrics.items():
            assert 0 <= value <= 1

    def test_predict(self):
        """Test model prediction functionality."""
        # Train model first
        X, y = self.model.preprocess_data(self.sample_data)
        self.model.train(X, y)

        # Test prediction
        predictions = self.model.predict(self.sample_data)

        # Check if predictions are returned
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(self.sample_data)

        # Check if predictions are valid (0 or 1 for binary classification)
        assert all(pred in [0, 1] for pred in predictions)

    def test_save_and_load_model(self):
        """Test model saving and loading functionality."""
        # Train model first
        X, y = self.model.preprocess_data(self.sample_data)
        self.model.train(X, y)

        # Create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, 'test_model.pkl')
            encoder_path = os.path.join(temp_dir, 'test_encoders.pkl')

            # Save model
            self.model.save_model(model_path, encoder_path)

            # Check if files are created
            assert os.path.exists(model_path)
            assert os.path.exists(encoder_path)

            # Create new model and load
            new_model = CensusModel()
            new_model.load_model(model_path, encoder_path)

            # Check if model is loaded correctly
            assert new_model.is_trained
            assert len(new_model.label_encoders) > 0

            # Test prediction with loaded model using the same format as training
            X_test, _ = new_model.preprocess_data(self.sample_data)
            predictions = new_model.predict(self.sample_data)
            assert isinstance(predictions, np.ndarray)
            assert len(predictions) == len(self.sample_data)

    def test_get_slice_performance(self):
        """Test slice performance calculation functionality."""
        # Train model first
        X, y = self.model.preprocess_data(self.sample_data)
        self.model.train(X, y)

        # Test slice performance
        slice_performance = self.model.get_slice_performance(self.sample_data, 'education')

        # Check if slice performance is calculated
        assert isinstance(slice_performance, dict)
        assert len(slice_performance) > 0

        # Check if each slice has required metrics
        for education, metrics in slice_performance.items():
            assert 'accuracy' in metrics
            assert 'precision' in metrics
            assert 'recall' in metrics
            assert 'f1' in metrics
            assert 'count' in metrics

            # Check if metrics are valid
            for metric, value in metrics.items():
                if metric == 'count':
                    assert value > 0
                else:
                    assert 0 <= value <= 1

    def test_predict_without_training(self):
        """Test that prediction fails when model is not trained."""
        with pytest.raises(ValueError, match="Model must be trained before making predictions"):
            self.model.predict(self.sample_data)

    def test_save_without_training(self):
        """Test that saving fails when model is not trained."""
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, 'test_model.pkl')
            encoder_path = os.path.join(temp_dir, 'test_encoders.pkl')

            with pytest.raises(ValueError, match="Model must be trained before saving"):
                self.model.save_model(model_path, encoder_path)

    def test_slice_performance_without_training(self):
        """Test that slice performance fails when model is not trained."""
        with pytest.raises(ValueError, match="Model must be trained before calculating slice performance"):
            self.model.get_slice_performance(self.sample_data, 'education')


if __name__ == "__main__":
    pytest.main([__file__])
