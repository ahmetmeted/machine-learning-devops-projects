"""
Logging and testing script for churn_library.py

Author: Your Name
Date: 2025-09-09
"""

import logging
from pathlib import Path
import pandas as pd
import churn_library as clib

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOGS_DIR / "churn_tests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)


def test_import_data():
    df = clib.import_data()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0
    LOGGER.info("test_import_data passed")
    return df


def test_perform_eda(df):
    clib.perform_eda(df)
    assert (Path("images/eda/churn_hist.png")).exists()
    LOGGER.info("test_perform_eda passed")


def test_encoder_helper(df):
    cat_cols = ["Gender", "Education_Level", "Marital_Status"]
    df2 = clib.encoder_helper(df, cat_cols, response="Churn")
    for col in cat_cols:
        assert col + "_Churn" in df2.columns
    LOGGER.info("test_encoder_helper passed")
    return df2


def test_perform_feature_engineering(df):
    X_train, X_test, y_train, y_test = clib.perform_feature_engineering(df, "Churn")
    assert X_train.shape[0] > 0
    assert X_test.shape[0] > 0
    LOGGER.info("test_perform_feature_engineering passed")
    return X_train, X_test, y_train, y_test


def test_train_models(X_train, X_test, y_train, y_test):
    clib.train_models(X_train, X_test, y_train, y_test)
    assert (Path("models/rf_model.pkl")).exists()
    assert (Path("models/lr_model.pkl")).exists()
    LOGGER.info("test_train_models passed")


if __name__ == "__main__":
    try:
        df = test_import_data()
        test_perform_eda(df)
        df2 = test_encoder_helper(df)
        X_tr, X_te, y_tr, y_te = test_perform_feature_engineering(df2)
        test_train_models(X_tr, X_te, y_tr, y_te)
        LOGGER.info("All tests passed ✅")
    except AssertionError as err:
        LOGGER.error("Test failed ❌: %s", err)
        raise
    except Exception as err:
        LOGGER.error("Unexpected error ❌: %s", err)
        raise
