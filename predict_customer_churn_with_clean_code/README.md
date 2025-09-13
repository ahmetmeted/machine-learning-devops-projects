# Credit Card Churn Prediction Project

## 📌 Description
This project identifies credit card customers who are most likely to churn.  
It refactors a provided notebook into a **production-quality Python package** with:
- Modular functions (`churn_library.py`)
- Logging and testing (`churn_script_logging_and_tests.py`)
- EDA plots, trained models, evaluation results saved to disk

## 🎯 Project Goals
- Implement clean code principles and best practices
- Create modular, maintainable Python code
- Implement comprehensive logging and testing
- Generate production-ready machine learning models
- Demonstrate MLOps best practices for model development

## 📂 Structure
```
.
├── churn_library.py
├── churn_script_logging_and_tests.py
├── README.md
├── data/bank_data.csv
├── images/
│   ├── eda/
│   └── results/
├── logs/
└── models/
```

## ▶️ Running
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the library end-to-end:
```bash
ipython churn_library.py
```

3. Run tests + logging:
```bash
ipython churn_script_logging_and_tests.py
```

Logs will be written to `logs/churn_library.log` and `logs/churn_tests.log`.

## 🧪 Tests
- `import_data`: Data loads correctly  
- `perform_eda`: EDA plots are generated  
- `encoder_helper`: Encoded columns added  
- `perform_feature_engineering`: Data split into train/test  
- `train_models`: Models trained, ROC curve, classification reports, feature importances saved  

## 📊 Outputs
- **EDA**: histograms, heatmap (`images/eda/`)  
- **Results**: ROC curves, classification reports, feature importance (`images/results/`)  
- **Models**: trained `.pkl` files (`models/`)  

## 📏 Code Quality
- PEP8 formatting:
```bash
autopep8 --in-place --aggressive --aggressive churn_library.py
autopep8 --in-place --aggressive --aggressive churn_script_logging_and_tests.py
```

- Lint check:
```bash
pylint churn_library.py
pylint churn_script_logging_and_tests.py
```

Target **pylint score ≥ 7**.

## ✅ Rubric Alignment
- Code quality: PEP8, docstrings, clear structure  
- Logging & Testing: implemented, stored in `/logs/`  
- Images & Models: saved in `images/` and `models/`  
- Problem solving: full ML workflow implemented

## 🐳 Docker Usage
```bash
# Build and run with Docker
docker build -t churn-prediction .
docker run -v $(pwd)/data:/app/data -v $(pwd)/images:/app/images -v $(pwd)/logs:/app/logs -v $(pwd)/models:/app/models churn-prediction
```

## 📋 Requirements
- Python 3.8+
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- joblib