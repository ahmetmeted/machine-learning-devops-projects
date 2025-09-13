# Model Card for Census Income Prediction Model

## Model Details
- **Model Name**: Census Income Prediction Model
- **Model Type**: Random Forest Classifier
- **Version**: 1.0
- **Date**: September 2024
- **Author**: ML Engineer
- **License**: MIT

## Intended Use
This model is designed to predict whether an individual's income exceeds $50,000 per year based on census data. The model is intended for educational and research purposes to demonstrate machine learning model deployment and API development.

### Primary Use Cases
- Educational demonstrations of ML model deployment
- Research on income prediction using census data
- API development and testing

### Out-of-Scope Use Cases
- Real-world financial decision making
- Employment screening
- Any commercial applications without proper validation

## Training Data
- **Dataset**: UCI Adult Census Income Dataset
- **Source**: UCI Machine Learning Repository
- **Size**: 32,561 samples
- **Features**: 14 demographic and economic features
- **Target**: Binary classification (>50K or <=50K income)

### Data Preprocessing
- Removed missing values (represented as '?')
- Cleaned whitespace from categorical variables
- Encoded categorical variables using LabelEncoder
- No feature scaling applied (Random Forest is scale-invariant)

### Data Splits
- Training set: 80% (26,048 samples)
- Test set: 20% (6,513 samples)
- Stratified split to maintain class distribution

## Performance Metrics
The model was evaluated using standard classification metrics:

### Overall Performance
- **Accuracy**: 0.85
- **Precision (Weighted)**: 0.84
- **Recall (Weighted)**: 0.85
- **F1-Score (Weighted)**: 0.84

### Performance by Education Level (Sample Slices)
- **Bachelors**: Accuracy 0.96, F1-Score 0.96 (5,044 samples)
- **HS-grad**: Accuracy 0.97, F1-Score 0.97 (9,840 samples)
- **11th**: Accuracy 0.99, F1-Score 0.99 (1,048 samples)

## Model Architecture
- **Algorithm**: Random Forest Classifier
- **Number of Estimators**: 100
- **Random State**: 42 (for reproducibility)
- **Feature Engineering**: Label encoding for categorical variables
- **No hyperparameter tuning performed**

## Limitations
- **Bias**: The model may reflect historical biases present in the training data
- **Temporal**: Trained on 1994 census data, may not reflect current economic conditions
- **Geographic**: Primarily US-focused data, limited international applicability
- **Feature Dependencies**: Model performance may vary significantly across different demographic groups

## Ethical Considerations
- **Fairness**: The model should not be used for discriminatory purposes
- **Privacy**: Input data should be handled according to privacy regulations
- **Transparency**: Model predictions should be explainable and auditable
- **Bias Mitigation**: Regular monitoring for biased predictions across different groups

## Recommendations
- Regular retraining with updated data
- Bias auditing across different demographic groups
- Performance monitoring in production
- Clear documentation of model limitations
- Regular validation against holdout datasets

## Model Monitoring
- Monitor prediction distribution shifts
- Track performance metrics over time
- Alert on significant accuracy drops
- Regular bias assessment across protected groups

## Contact Information
For questions about this model, please contact the development team or refer to the project repository.





