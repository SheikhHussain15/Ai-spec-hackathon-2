#!/usr/bin/env python
"""
Complete test of the task creation flow
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_full_flow():
    """Test complete registration, login, and task creation flow"""
    print("=" * 60)
    print("COMPLETE AUTH + TASK CREATION TEST")
    print("=" * 60)
    
    # Step 1: Register
    print("\n[Step 1] Registering new user...")
    unique_email = f"test_flow_{int(time.time())}@example.com"
    signup_data = {
        "email": unique_email,
        "name": "Flow Test User",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=signup_data, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  [FAIL] Registration failed: {response.json()}")
            return False
        
        user_data = response.json()
        user_id = user_data.get('id')
        print(f"  [PASS] User created: {user_id}")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False
    
    # Step 2: Login
    print("\n[Step 2] Logging in...")
    login_data = {
        "email": unique_email,
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  [FAIL] Login failed: {response.json()}")
            return False
        
        token = response.json().get('access_token')
        if not token:
            print(f"  [FAIL] No token in response")
            return False
        
        print(f"  [PASS] Token received: {token[:50]}...")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False
    
    # Step 3: Get tasks (should be empty)
    print("\n[Step 3] Fetching tasks (should be empty)...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/tasks", headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  [FAIL] Get tasks failed: {response.json()}")
            return False
        
        tasks = response.json()
        print(f"  [PASS] Got {len(tasks)} tasks")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False
    
    # Step 4: Create a task
    print("\n[Step 4] Creating a new task...")
    task_data = {
        "title": "My First Task",
        "description": "This is a test task created via API"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  [FAIL] Task creation failed: {response.json()}")
            return False
        
        task = response.json()
        task_id = task.get('id')
        print(f"  [PASS] Task created: {task_id}")
        print(f"  Task details: title='{task.get('title')}', completed={task.get('completed')}")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False
    
    # Step 5: Get tasks again (should have 1 task)
    print("\n[Step 5] Fetching tasks again (should have 1 task)...")
    
    try:
        response = requests.get(f"{BASE_URL}/tasks", headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  [FAIL] Get tasks failed: {response.json()}")
            return False
        
        tasks = response.json()
        print(f"  [PASS] Got {len(tasks)} task(s)")
        
        if len(tasks) != 1:
            print(f"  [WARN] Expected 1 task, got {len(tasks)}")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False
    
    # Step 6: Toggle task completion
    print("\n[Step 6] Toggling task completion...")
    
    try:
        response = requests.patch(f"{BASE_URL}/tasks/{task_id}/toggle", headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  [FAIL] Toggle failed: {response.json()}")
            return False
        
        updated_task = response.json()
        print(f"  [PASS] Task toggled: completed={updated_task.get('completed')}")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False
    
    # Step 7: Delete task
    print("\n[Step 7] Deleting task...")
    
    try:
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code != 204:
            print(f"  [FAIL] Delete failed with status: {response.status_code}")
            return False
        
        print(f"  [PASS] Task deleted")
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    print("Waiting for backend to be ready...")
    time.sleep(2)
    
    success = test_full_flow()
    exit(0 if success else 1)
