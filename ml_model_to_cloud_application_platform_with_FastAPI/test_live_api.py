#!/usr/bin/env python3
"""
Live API testing script for the Census Income Prediction API
"""

import requests
import json
import sys


def test_live_api(base_url="http://localhost:8000"):
    """
    Test the live API endpoints.

    Args:
        base_url (str): Base URL of the API
    """
    print(f"Testing API at: {base_url}")
    print("=" * 50)

    # Test GET endpoint
    print("Testing GET / endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            print("✓ GET endpoint test passed")
        else:
            print(f"✗ GET endpoint test failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ GET endpoint test failed: {e}")
        return False

    print("\n" + "=" * 50)

    # Test POST endpoint with high income prediction
    print("Testing POST /predict endpoint (high income case)...")
    test_data_high = {
        "age": 45,
        "workclass": "Private",
        "fnlgt": 2334,
        "education": "Bachelors",
        "education-num": 13,
        "marital-status": "Married-civ-spouse",
        "occupation": "Exec-managerial",
        "relationship": "Husband",
        "race": "White",
        "sex": "Male",
        "capital-gain": 15000,
        "capital-loss": 0,
        "hours-per-week": 40,
        "native-country": "United-States"
    }

    try:
        response = requests.post(f"{base_url}/predict", json=test_data_high)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            print("✓ POST endpoint test (high income) passed")
        else:
            print(f"✗ POST endpoint test (high income) failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ POST endpoint test (high income) failed: {e}")
        return False

    print("\n" + "=" * 50)

    # Test POST endpoint with low income prediction
    print("Testing POST /predict endpoint (low income case)...")
    test_data_low = {
        "age": 25,
        "workclass": "Private",
        "fnlgt": 1234,
        "education": "HS-grad",
        "education-num": 9,
        "marital-status": "Never-married",
        "occupation": "Handlers-cleaners",
        "relationship": "Not-in-family",
        "race": "Black",
        "sex": "Female",
        "capital-gain": 0,
        "capital-loss": 0,
        "hours-per-week": 20,
        "native-country": "United-States"
    }

    try:
        response = requests.post(f"{base_url}/predict", json=test_data_low)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            print("✓ POST endpoint test (low income) passed")
        else:
            print(f"✗ POST endpoint test (low income) failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ POST endpoint test (low income) failed: {e}")
        return False

    print("\n" + "=" * 50)
    print("✓ All tests passed!")
    return True


def main():
    """Main function."""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8000"

    success = test_live_api(base_url)

    if success:
        print("\n🎉 All API tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some API tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
