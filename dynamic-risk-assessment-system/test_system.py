#!/usr/bin/env python3
"""
Test script to verify the dynamic risk assessment system is working correctly
"""

import os
import sys
import json
import pandas as pd
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_data_ingestion():
    """Test data ingestion functionality"""
    logger.info("Testing data ingestion...")
    result = subprocess.run([sys.executable, 'ingestion.py'], capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("✓ Data ingestion test passed")
        return True
    else:
        logger.error(f"✗ Data ingestion test failed: {result.stderr}")
        return False

def test_model_training():
    """Test model training functionality"""
    logger.info("Testing model training...")
    result = subprocess.run([sys.executable, 'training.py'], capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("✓ Model training test passed")
        return True
    else:
        logger.error(f"✗ Model training test failed: {result.stderr}")
        return False

def test_model_scoring():
    """Test model scoring functionality"""
    logger.info("Testing model scoring...")
    result = subprocess.run([sys.executable, 'scoring.py'], capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("✓ Model scoring test passed")
        return True
    else:
        logger.error(f"✗ Model scoring test failed: {result.stderr}")
        return False

def test_model_deployment():
    """Test model deployment functionality"""
    logger.info("Testing model deployment...")
    result = subprocess.run([sys.executable, 'deployment.py'], capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("✓ Model deployment test passed")
        return True
    else:
        logger.error(f"✗ Model deployment test failed: {result.stderr}")
        return False

def test_diagnostics():
    """Test diagnostics functionality"""
    logger.info("Testing diagnostics...")
    result = subprocess.run([sys.executable, 'diagnostics.py'], capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("✓ Diagnostics test passed")
        return True
    else:
        logger.error(f"✗ Diagnostics test failed: {result.stderr}")
        return False

def test_reporting():
    """Test reporting functionality"""
    logger.info("Testing reporting...")
    result = subprocess.run([sys.executable, 'reporting.py'], capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("✓ Reporting test passed")
        return True
    else:
        logger.error(f"✗ Reporting test failed: {result.stderr}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    logger.info("Testing file structure...")
    
    required_files = [
        'config.json',
        'requirements.txt',
        'ingestion.py',
        'training.py',
        'scoring.py',
        'deployment.py',
        'diagnostics.py',
        'reporting.py',
        'app.py',
        'apicalls.py',
        'fullprocess.py',
        'wsgi.py',
        'cronjob.txt',
        'README.md'
    ]
    
    required_dirs = [
        'sourcedata',
        'testdata',
        'ingesteddata',
        'models',
        'production_deployment'
    ]
    
    all_files_exist = True
    for file in required_files:
        if not os.path.exists(file):
            logger.error(f"✗ Required file missing: {file}")
            all_files_exist = False
        else:
            logger.info(f"✓ Found: {file}")
    
    for dir in required_dirs:
        if not os.path.isdir(dir):
            logger.error(f"✗ Required directory missing: {dir}")
            all_files_exist = False
        else:
            logger.info(f"✓ Found directory: {dir}")
    
    if all_files_exist:
        logger.info("✓ File structure test passed")
    else:
        logger.error("✗ File structure test failed")
    
    return all_files_exist

def test_data_files():
    """Test that data files exist and are readable"""
    logger.info("Testing data files...")
    
    # Test sourcedata
    sourcedata_files = os.listdir('sourcedata')
    if len(sourcedata_files) > 0:
        logger.info(f"✓ Found {len(sourcedata_files)} files in sourcedata")
    else:
        logger.error("✗ No files found in sourcedata")
        return False
    
    # Test testdata
    testdata_files = os.listdir('testdata')
    if len(testdata_files) > 0:
        logger.info(f"✓ Found {len(testdata_files)} files in testdata")
    else:
        logger.error("✗ No files found in testdata")
        return False
    
    # Test that we can read the data
    try:
        df = pd.read_csv('testdata/testdata.csv')
        logger.info(f"✓ Test data readable: {df.shape}")
    except Exception as e:
        logger.error(f"✗ Cannot read test data: {e}")
        return False
    
    logger.info("✓ Data files test passed")
    return True

def main():
    """Run all tests"""
    logger.info("Starting system tests...")
    
    tests = [
        ("File Structure", test_file_structure),
        ("Data Files", test_data_files),
        ("Data Ingestion", test_data_ingestion),
        ("Model Training", test_model_training),
        ("Model Scoring", test_model_scoring),
        ("Model Deployment", test_model_deployment),
        ("Diagnostics", test_diagnostics),
        ("Reporting", test_reporting)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Running {test_name} Test ---")
        if test_func():
            passed += 1
        else:
            logger.error(f"{test_name} test failed!")
    
    logger.info(f"\n--- Test Results ---")
    logger.info(f"Passed: {passed}/{total}")
    
    if passed == total:
        logger.info("🎉 All tests passed! System is ready for use.")
        return True
    else:
        logger.error(f"❌ {total - passed} tests failed. Please check the errors above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

