#!/usr/bin/env python3
"""Simple API test script to verify models are loading and endpoints work."""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_models():
    """Test GET /models to verify models are available."""
    print("\n=== Testing GET /models ===")
    try:
        response = requests.get(f"{BASE_URL}/models", timeout=5)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print(f"✅ PASS - Found {len(data)} models")
            for model in data:
                print(f"   - {model.get('dataset_name')}: {model.get('model_type')}")
            return True
        else:
            print(f"❌ FAIL")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_predict():
    """Test POST /predict with auto model selection."""
    print("\n=== Testing POST /predict (with auto selection) ===")
    try:
        payload = {
            "features": {
                "feature_0": 1.0,
                "feature_1": 2.0,
                "feature_2": 3.0
            }
        }
        response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=5)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print(f"✅ PASS - Prediction: {data.get('prediction')}")
            return True
        else:
            print(f"❌ FAIL - {data.get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_predict_with_model():
    """Test POST /predict with specific model."""
    print("\n=== Testing POST /predict (with dataset3) ===")
    try:
        payload = {
            "features": {
                "feature_0": 1.0,
                "feature_1": 2.0,
                "feature_2": 3.0
            },
            "model_name": "dataset3"
        }
        response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=5)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print(f"✅ PASS - Prediction: {data.get('prediction')}")
            return True
        else:
            print(f"❌ FAIL - {data.get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_ingest():
    """Test POST /ingest with sensor data."""
    print("\n=== Testing POST /ingest ===")
    try:
        payload = {
            "sensor_id": "SENSOR_001",
            "sensor_type": "flow_meter",
            "parameter_name": "flow_rate",
            "value": 1000.5,
            "unit": "LPM"
        }
        response = requests.post(f"{BASE_URL}/ingest", json=payload, timeout=5)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code in [200, 201]:
            print(f"✅ PASS")
            return True
        else:
            print(f"❌ FAIL - {data.get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Starting API tests...")
    print("Waiting 3 seconds for backend to be ready...")
    time.sleep(3)
    
    results = []
    results.append(("GET /models", test_models()))
    results.append(("POST /predict (auto)", test_predict()))
    results.append(("POST /predict (dataset3)", test_predict_with_model()))
    results.append(("POST /ingest", test_ingest()))
    
    print("\n=== SUMMARY ===")
    passed = sum(1 for _, result in results if result)
    print(f"Passed: {passed}/{len(results)}")
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
