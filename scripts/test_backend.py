"""
Quick test script for backend API
"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def test_endpoint(path, method="GET", data=None):
    """Test an API endpoint."""
    url = f"{BASE_URL}{path}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        print(f"✓ {method} {path}: Status {response.status_code}")
        if response.status_code == 200:
            print(f"  Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print(f"✗ {method} {path}: Connection refused (server not running?)")
        return False
    except Exception as e:
        print(f"✗ {method} {path}: Error - {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing SIH WATER AI Backend API")
    print("=" * 60)
    
    # Test root endpoint
    print("\n1. Testing Root Endpoint...")
    test_endpoint("/")
    
    # Test health endpoint
    print("\n2. Testing Health Endpoint...")
    test_endpoint("/api/health")
    
    # Test models endpoint
    print("\n3. Testing Models List Endpoint...")
    test_endpoint("/api/models")
    
    print("\n" + "=" * 60)
    print("Backend Test Complete!")
    print("=" * 60)

