import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import engine
from sqlmodel import SQLModel, Session
from unittest.mock import patch

client = TestClient(app)

def test_login_endpoint_contract():
    """
    Contract test for login endpoint
    """
    # Test that the endpoint exists and accepts the expected parameters
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    
    # The endpoint should return 401 for invalid credentials
    # or 422 for validation errors if the request format is incorrect
    assert response.status_code in [401, 422]

def test_register_endpoint_contract():
    """
    Contract test for register endpoint
    """
    # Test that the endpoint exists and accepts the expected parameters
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "securepassword123"
        }
    )
    
    # The endpoint should return 400 for invalid input or already existing user
    # or 422 for validation errors if the request format is incorrect
    # or 200 for successful registration
    assert response.status_code in [200, 400, 422]

def test_get_user_tasks_contract():
    """
    Contract test for user tasks endpoint
    """
    # Test that the endpoint exists and requires authentication
    response = client.get("/api/users/test-user-id/tasks")
    
    # Should return 401 for missing/invalid authentication
    assert response.status_code == 401

def test_create_user_task_contract():
    """
    Contract test for creating user task endpoint
    """
    # Test that the endpoint exists and requires authentication
    response = client.post(
        "/api/users/test-user-id/tasks",
        json={
            "title": "Test task",
            "description": "Test description",
            "completed": False,
            "user_id": "test-user-id"
        }
    )
    
    # Should return 401 for missing/invalid authentication
    assert response.status_code == 401