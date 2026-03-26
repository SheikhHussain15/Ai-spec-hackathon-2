#!/usr/bin/env python
"""
Test script to verify login and signup endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_signup():
    """Test user registration"""
    print("=" * 50)
    print("Testing Signup...")
    print("=" * 50)
    
    signup_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=signup_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✓ Signup successful!")
            return True
        else:
            print("✗ Signup failed!")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\n" + "=" * 50)
    print("Testing Login...")
    print("=" * 50)
    
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✓ Login successful! Token: {token[:50]}...")
            return True
        else:
            print("✗ Login failed!")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("Auth Endpoint Tester")
    print("Make sure the backend server is running on http://localhost:8000")
    print("\nPress Enter to start tests...")
    input()
    
    test_signup()
    test_login()
