#!/usr/bin/env python3
"""
Complete API Testing Script for SIH WATER AI
Tests all endpoints and features
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"

def test_endpoint(method, endpoint, data=None, name="Test"):
    """Test an endpoint and print results."""
    url = f"{BASE_URL}{API_PREFIX}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            return False
        
        status = "✅ PASS" if response.status_code < 400 else "❌ FAIL"
        print(f"{status} | {method:6} | {endpoint:40} | Status: {response.status_code}")
        
        if response.status_code >= 400:
            print(f"       Error: {response.text[:100]}")
        return response.status_code < 400
    except Exception as e:
        print(f"❌ FAIL | {method:6} | {endpoint:40} | Error: {str(e)[:50]}")
        return False

def main():
    print("=" * 100)
    print("SIH WATER AI - API Testing Report")
    print("=" * 100)
    print()
    
    results = {
        "Health Check": [],
        "Sensor Data": [],
        "Predictions": [],
        "Models": [],
        "Reports": [],
    }
    
    # 1. Health Check
    print("1️⃣  HEALTH CHECK")
    print("-" * 100)
    results["Health Check"].append(test_endpoint("GET", "/health", name="Health Check"))
    print()
    
    # 2. Sensor Data
    print("2️⃣  SENSOR DATA ENDPOINTS")
    print("-" * 100)
    results["Sensor Data"].append(test_endpoint("GET", "/sensors/recent?limit=10", name="Get Recent Sensors"))
    results["Sensor Data"].append(test_endpoint("POST", "/ingest", {
        "sensor_id": "test_sensor_1",
        "parameter_name": "Turbidity",
        "value": 35.5,
        "unit": "%"
    }, name="Ingest Sensor Data"))
    print()
    
    # 3. Twin Status
    print("3️⃣  DIGITAL TWIN")
    print("-" * 100)
    results["Predictions"].append(test_endpoint("GET", "/twin_status", name="Get Twin Status"))
    print()
    
    # 4. Predictions
    print("4️⃣  ML PREDICTION ENDPOINTS")
    print("-" * 100)
    results["Predictions"].append(test_endpoint("GET", "/predictions/recent?limit=5", name="Get Recent Predictions"))
    
    # Test prediction with sample data
    sample_features = {
        "ph": 7.5,
        "Hardness": 200,
        "Solids": 20000,
        "Chloramines": 4,
        "Sulfate": 333,
        "Conductivity": 750,
        "Organic_carbon": 12,
        "Trihalomethanes": 70,
        "Turbidity": 5
    }
    
    results["Predictions"].append(test_endpoint("POST", "/predict", {
        "features": sample_features,
        "model_name": "auto"
    }, name="Make ML Prediction"))
    print()
    
    # 5. Models
    print("5️⃣  MODEL MANAGEMENT ENDPOINTS")
    print("-" * 100)
    results["Models"].append(test_endpoint("GET", "/models", name="List Models"))
    print()
    
    # 6. Reports
    print("6️⃣  REPORT GENERATION")
    print("-" * 100)
    results["Reports"].append(test_endpoint("POST", "/report", {
        "title": "Test Report",
        "include_charts": True
    }, name="Generate Report"))
    print()
    
    # Summary
    print("=" * 100)
    print("TEST SUMMARY")
    print("=" * 100)
    
    total_tests = 0
    total_passed = 0
    
    for category, tests in results.items():
        passed = sum(1 for t in tests if t)
        total = len(tests)
        total_tests += total
        total_passed += passed
        status = "✅" if passed == total else "⚠️"
        print(f"{status} {category:30} | {passed}/{total} tests passed")
    
    print()
    print(f"TOTAL: {total_passed}/{total_tests} tests passed ({(total_passed/total_tests)*100:.1f}%)")
    print()
    
    if total_passed == total_tests:
        print("🎉 ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION! 🎉")
    else:
        print(f"⚠️  {total_tests - total_passed} test(s) failed - Review errors above")
    
    print()
    print("=" * 100)
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)

if __name__ == "__main__":
    time.sleep(2)  # Wait for servers to be ready
    main()
