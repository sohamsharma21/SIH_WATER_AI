"""
End-to-end system test script
Tests backend API and verifies frontend connectivity
"""
import requests
import json
import time
from typing import Dict, Any

BACKEND_URL = "http://localhost:8000/api/v1"

def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def test_backend_health():
    """Test backend health endpoint."""
    print_section("Testing Backend Health")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✓ Backend is healthy")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend")
        print("  Make sure backend is running: python -m uvicorn backend.app.main:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_models_endpoint():
    """Test models endpoint."""
    print_section("Testing Models Endpoint")
    try:
        response = requests.get(f"{BACKEND_URL}/models", timeout=10)
        if response.status_code == 200:
            data = response.json()
            manager_models = data.get('manager_models', [])
            db_models = data.get('database_models', [])
            print(f"✓ Models endpoint working")
            print(f"  Manager models: {len(manager_models)}")
            print(f"  Database models: {len(db_models)}")
            if manager_models:
                for model in manager_models:
                    print(f"    - {model.get('dataset_name')}: {model.get('model_type')}")
            return True
        else:
            print(f"✗ Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_prediction_dataset2():
    """Test prediction with Dataset 2."""
    print_section("Testing Prediction - Dataset 2 (Water Potability)")
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
            f"{BACKEND_URL}/predict",
            json=payload,
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            prediction = data.get('prediction', {})
            print("✓ Prediction successful")
            print(f"  Model: {prediction.get('model_name')}")
            print(f"  Prediction: {prediction.get('prediction')}")
            print(f"  Quality Score: {prediction.get('quality_score')}%")
            print(f"  Contamination Index: {prediction.get('contamination_index')}%")
            if prediction.get('confidence'):
                print(f"  Confidence: {prediction.get('confidence') * 100:.1f}%")
            return True
        else:
            print(f"✗ Status code: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_prediction_dataset3():
    """Test prediction with Dataset 3."""
    print_section("Testing Prediction - Dataset 3 (UCI Treatment)")
    # Create features for dataset3
    features = {}
    for i in range(1, 38):
        features[f"feature_{i}"] = 100.0 + (i * 10)
    
    payload = {
        "features": features,
        "model_name": "dataset3",
        "use_ensemble": False
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/predict",
            json=payload,
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            prediction = data.get('prediction', {})
            print("✓ Prediction successful")
            print(f"  Model: {prediction.get('model_name')}")
            print(f"  Prediction: {prediction.get('prediction'):.2f}")
            print(f"  Quality Score: {prediction.get('quality_score'):.2f}%")
            return True
        else:
            print(f"✗ Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_sensor_ingest():
    """Test sensor data ingestion."""
    print_section("Testing Sensor Data Ingestion")
    payload = {
        "sensor_id": "test_sensor_001",
        "sensor_type": "pH",
        "parameter_name": "pH",
        "value": 7.2,
        "unit": "pH",
        "location": "Primary Treatment"
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/ingest",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print("✓ Sensor data ingested successfully")
            print(f"  Sensor ID: {data.get('sensor_id')}")
            return True
        else:
            print(f"✗ Status code: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_twin_status():
    """Test digital twin status endpoint."""
    print_section("Testing Digital Twin Status")
    try:
        response = requests.get(f"{BACKEND_URL}/twin_status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✓ Twin status retrieved")
            print(f"  Sensors: {len(data.get('sensor_status', {}))}")
            print(f"  Latest prediction: {data.get('latest_prediction') is not None}")
            return True
        else:
            print(f"✗ Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("SIH WATER AI - Full System Test")
    print("=" * 60)
    print("\nMake sure backend is running on http://localhost:8000")
    print("=" * 60)
    
    results = {}
    
    # Test backend connectivity
    if not test_backend_health():
        print("\n⚠ Backend is not running. Please start it first.")
        print("  Command: python -m uvicorn backend.app.main:app --reload --port 8000")
        return
    
    # Run tests
    results['models'] = test_models_endpoint()
    results['prediction_dataset2'] = test_prediction_dataset2()
    results['prediction_dataset3'] = test_prediction_dataset3()
    results['sensor_ingest'] = test_sensor_ingest()
    results['twin_status'] = test_twin_status()
    
    # Summary
    print_section("Test Summary")
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! System is ready.")
    else:
        print("\n⚠ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()

