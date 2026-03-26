import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import engine
from sqlmodel import SQLModel, Session
from unittest.mock import patch
from src.models.user import User
from src.services.auth_service import AuthService
from src.auth.jwt_utils import create_access_token

client = TestClient(app)

def test_login_to_api_request_flow():
    """
    Integration test for login → token → API request flow
    """
    # First, register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "integration_test@example.com",
            "password": "securepassword123"
        }
    )
    
    assert register_response.status_code == 200
    register_data = register_response.json()
    user_id = register_data["id"]
    
    # Then, log in to get a token
    login_response = client.post(
        "/api/auth/login",
        data={
            "email": "integration_test@example.com",
            "password": "securepassword123"
        }
    )
    
    assert login_response.status_code == 200
    login_data = login_response.json()
    token = login_data["access_token"]
    
    # Use the token to make an authenticated request
    headers = {"Authorization": f"Bearer {token}"}
    api_response = client.get(f"/api/users/{user_id}", headers=headers)
    
    assert api_response.status_code == 200
    user_data = api_response.json()
    assert user_data["email"] == "integration_test@example.com"
    assert user_data["id"] == user_id

def test_invalid_token_rejection():
    """
    Integration test to ensure invalid tokens are rejected
    """
    # Use an obviously invalid token
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = client.get("/api/users/test-user-id", headers=headers)
    
    assert response.status_code == 401

def test_expired_token_rejection():
    """
    Integration test to ensure expired tokens are rejected
    """
    # Create an expired token
    expired_token = create_access_token(
        data={"user_id": "test_user", "email": "test@example.com"},
        expires_delta=-1  # Expired 1 second ago
    )
    
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/api/users/test_user", headers=headers)
    
    assert response.status_code == 401