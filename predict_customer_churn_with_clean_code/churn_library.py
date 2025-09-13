"""
Churn prediction library.

Implements data import, EDA, feature engineering, model training,
prediction and evaluation.

Author: [Your Name]
Date: 2025-09-09
"""

import logging
from pathlib import Path
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, RocCurveDisplay
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Paths
DATA_PTH = Path("data/bank_data.csv")
EDA_DIR = Path("images/eda")
RESULTS_DIR = Path("images/results")
MODELS_DIR = Path("models")
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True, parents=True)
EDA_DIR.mkdir(exist_ok=True, parents=True)
RESULTS_DIR.mkdir(exist_ok=True, parents=True)
MODELS_DIR.mkdir(exist_ok=True, parents=True)

# Logging
logging.basicConfig(
    filename=LOGS_DIR / "churn_library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)


def import_data(pth=DATA_PTH):
    """
    returns dataframe for the csv found at pth
    """
    try:
        df = pd.read_csv(pth)
        LOGGER.info("Data imported successfully with shape %s", df.shape)
        return df
    except Exception as err:
        LOGGER.error("Error importing data: %s", err)
        raise


def perform_eda(df):
    """
    perform eda on df and save figures to images/eda folder
    """
    try:
        plt.figure(figsize=(8, 6))
        df["Churn"].hist()
        plt.savefig(EDA_DIR / "churn_hist.png")
        plt.close()

        plt.figure(figsize=(8, 6))
        df["Customer_Age"].hist()
        plt.savefig(EDA_DIR / "age_hist.png")
        plt.close()

        plt.figure(figsize=(8, 6))
        sns.heatmap(df.corr(numeric_only=True), annot=False, cmap="viridis")
        plt.savefig(EDA_DIR / "heatmap.png")
        plt.close()

        LOGGER.info("EDA completed and images saved")
    except Exception as err:
        LOGGER.error("EDA failed: %s", err)
        raise


def encoder_helper(df, category_lst, response="Churn"):
    """
    helper function to turn each categorical column into a new column with
    proportion of churn for each category
    """
    try:
        for col in category_lst:
            means = df.groupby(col)[response].mean()
            df[col + "_" + response] = df[col].map(means)
        LOGGER.info("Encoding completed on %s", category_lst)
        return df
    except Exception as err:
        LOGGER.error("Encoding failed: %s", err)
        raise


def perform_feature_engineering(df, response="Churn"):
    """
    split data into train and test sets
    """
    try:
        y = df[response]
        X = df.drop(columns=[response])

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        LOGGER.info("Data split into train and test")
        return X_train, X_test, y_train, y_test
    except Exception as err:
        LOGGER.error("Feature engineering failed: %s", err)
        raise


def classification_report_image(
    y_train, y_test, y_train_preds_lr, y_train_preds_rf,
    y_test_preds_lr, y_test_preds_rf
):
    """
    produces classification report for training and testing results
    and stores report as image
    """
    try:
        plt.figure(figsize=(10, 8))
        plt.text(0.01, 1.25, str('Random Forest Train'), fontsize=10)
        plt.text(0.01, 1.05, str(classification_report(y_train, y_train_preds_rf)), fontsize=10)
        plt.text(0.01, 0.6, str('Random Forest Test'), fontsize=10)
        plt.text(0.01, 0.4, str(classification_report(y_test, y_test_preds_rf)), fontsize=10)

        plt.text(0.01, -0.1, str('Logistic Regression Train'), fontsize=10)
        plt.text(0.01, -0.3, str(classification_report(y_train, y_train_preds_lr)), fontsize=10)
        plt.text(0.01, -0.7, str('Logistic Regression Test'), fontsize=10)
        plt.text(0.01, -0.9, str(classification_report(y_test, y_test_preds_lr)), fontsize=10)

        plt.axis('off')
        plt.savefig(RESULTS_DIR / "classification_report.png")
        plt.close()
        LOGGER.info("Classification report saved")
    except Exception as err:
        LOGGER.error("Classification report failed: %s", err)
        raise


def feature_importance_plot(model, X_data, output_pth):
    """
    creates and stores the feature importances
    """
    try:
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        names = [X_data.columns[i] for i in indices]

        plt.figure(figsize=(10, 6))
        plt.title("Feature Importance")
        plt.bar(range(X_data.shape[1]), importances[indices])
        plt.xticks(range(X_data.shape[1]), names, rotation=90)
        plt.savefig(output_pth)
        plt.close()
        LOGGER.info("Feature importance plot saved")
    except Exception as err:
        LOGGER.error("Feature importance plot failed: %s", err)
        raise


def train_models(X_train, X_test, y_train, y_test):
    """
    train, store model results: images + scores, and store models
    """
    try:
        rf = RandomForestClassifier(random_state=42)
        lr = LogisticRegression(max_iter=1000)

        rf.fit(X_train, y_train)
        lr.fit(X_train, y_train)

        y_train_preds_rf = rf.predict(X_train)
        y_test_preds_rf = rf.predict(X_test)
        y_train_preds_lr = lr.predict(X_train)
        y_test_preds_lr = lr.predict(X_test)

        classification_report_image(
            y_train, y_test,
            y_train_preds_lr, y_train_preds_rf,
            y_test_preds_lr, y_test_preds_rf
        )

        RocCurveDisplay.from_estimator(rf, X_test, y_test)
        RocCurveDisplay.from_estimator(lr, X_test, y_test)
        plt.savefig(RESULTS_DIR / "roc_curves.png")
        plt.close()

        feature_importance_plot(rf, X_train, RESULTS_DIR / "feature_importance.png")

        joblib.dump(rf, MODELS_DIR / "rf_model.pkl")
        joblib.dump(lr, MODELS_DIR / "lr_model.pkl")
        LOGGER.info("Models trained and saved")
    except Exception as err:
        LOGGER.error("Training failed: %s", err)
        raise
