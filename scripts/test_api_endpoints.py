"""
Test script for API endpoints
"""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test health check endpoint."""
    print("=" * 60)
    print("Testing /health")
    print("=" * 60)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_get_models():
    """Test get models endpoint."""
    print("\n" + "=" * 60)
    print("Testing /models")
    print("=" * 60)
    try:
        response = requests.get(f"{BASE_URL}/models")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Manager Models: {len(data.get('manager_models', []))}")
        print(f"Database Models: {len(data.get('database_models', []))}")
        if data.get('manager_models'):
            for model in data['manager_models']:
                print(f"  - {model.get('dataset_name')}: {model.get('model_type')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_predict_dataset2():
    """Test prediction with Dataset 2 (Water Potability)."""
    print("\n" + "=" * 60)
    print("Testing /predict_with (Dataset 2 - Water Potability)")
    print("=" * 60)
    
    # Sample features for water potability
    features = {
        "ph": 7.0,
        "Hardness": 200.0,
        "Solids": 20000.0,
        "Chloramines": 7.0,
        "Sulfate": 300.0,
        "Conductivity": 400.0,
        "Organic_carbon": 10.0,
        "Trihalomethanes": 50.0,
        "Turbidity": 3.0
    }
    
    payload = {
        "features": features,
        "model_name": "dataset2",
        "use_ensemble": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict_with",
            json=payload
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Prediction: {json.dumps(data, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_predict_dataset3():
    """Test prediction with Dataset 3 (UCI Water Treatment)."""
    print("\n" + "=" * 60)
    print("Testing /predict_with (Dataset 3 - UCI)")
    print("=" * 60)
    
    # Sample features - using feature_0 to feature_37
    features = {}
    for i in range(38):
        features[f"feature_{i}"] = 100.0 + (i * 10)  # Sample values
    
    payload = {
        "features": features,
        "model_name": "dataset3",
        "use_ensemble": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict_with",
            json=payload
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Prediction: {json.dumps(data, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_predict_dataset4():
    """Test prediction with Dataset 4 (Melbourne WWTP)."""
    print("\n" + "=" * 60)
    print("Testing /predict_with (Dataset 4 - Melbourne WWTP)")
    print("=" * 60)
    
    # Sample features for Melbourne WWTP
    features = {
        "Average Outflow": 3.0,
        "Average Inflow": 3.0,
        "Energy Consumption": 200000.0,
        "Ammonia": 30.0,
        "Chemical Oxygen Demand": 800.0,
        "Total Nitrogen": 60.0,
        "Average Temperature": 20.0,
        "Maximum temperature": 25.0,
        "Minimum temperature": 15.0,
        "Atmospheric pressure": 0.0,
        "Average humidity": 50.0,
        "Total rainfall": 0.0,
        "Average visibility": 10.0,
        "Average wind speed": 20.0,
        "Maximum wind speed": 50.0,
        "Year": 2024.0,
        "Month": 1.0,
        "Day": 1.0
    }
    
    payload = {
        "features": features,
        "model_name": "dataset4",
        "use_ensemble": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict_with",
            json=payload
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Prediction: {json.dumps(data, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_ingest_sensor():
    """Test sensor data ingestion."""
    print("\n" + "=" * 60)
    print("Testing /ingest (Sensor Data)")
    print("=" * 60)
    
    payload = {
        "sensor_id": "sensor_001",
        "sensor_type": "pH",
        "parameter_name": "pH",
        "value": 7.2,
        "unit": "pH",
        "location": "Primary Treatment"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/ingest",
            json=payload
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("SIH WATER AI - API Endpoint Tests")
    print("=" * 60)
    print("\nMake sure the backend server is running on http://localhost:8000")
    print("=" * 60)
    
    results = {}
    
    results['health'] = test_health()
    results['models'] = test_get_models()
    results['predict_dataset2'] = test_predict_dataset2()
    results['predict_dataset3'] = test_predict_dataset3()
    results['predict_dataset4'] = test_predict_dataset4()
    results['ingest'] = test_ingest_sensor()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")

if __name__ == "__main__":
    main()

