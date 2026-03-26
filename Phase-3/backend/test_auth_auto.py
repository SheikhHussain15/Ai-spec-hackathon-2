#!/usr/bin/env python
"""
Test script to verify login and signup endpoints
"""
import requests
import json
import time
import uuid

BASE_URL = "http://localhost:8000/api"

def test_health():
    """Check if server is running"""
    print("Checking server health...")
    try:
        response = requests.get(f"{BASE_URL.replace('/api', '')}/health", timeout=5)
        print(f"Server Status: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Server not responding: {e}")
        return False

def test_signup():
    """Test user registration"""
    print("\n" + "=" * 50)
    print("Testing Signup...")
    print("=" * 50)
    
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    signup_data = {
        "email": unique_email,
        "name": "Test User",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=signup_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("[PASS] Signup successful!")
            return unique_email
        else:
            print("[FAIL] Signup failed!")
            return None
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return None

def test_login(email, password="testpass123"):
    """Test user login"""
    print("\n" + "=" * 50)
    print("Testing Login...")
    print("=" * 50)
    
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"[PASS] Login successful! Token: {token[:50]}...")
            return True
        else:
            print("[FAIL] Login failed!")
            return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

if __name__ == "__main__":
    print("Auth Endpoint Tester")
    
    # Wait for server to be ready
    print("Waiting for server to start...")
    time.sleep(2)
    
    if not test_health():
        print("\n[FAIL] Server is not running! Please start the backend server first.")
        exit(1)
    
    email = test_signup()
    if email:
        test_login(email)
