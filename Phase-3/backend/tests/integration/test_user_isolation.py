import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import engine
from sqlmodel import SQLModel, Session
from unittest.mock import patch
from src.models.user import User

client = TestClient(app)

def test_user_isolation():
    """
    Integration test for user isolation - ensure users can't access other users' data
    """
    # Register first user
    user1_response = client.post(
        "/api/auth/register",
        json={
            "email": "user1@example.com",
            "password": "securepassword123"
        }
    )
    assert user1_response.status_code == 200
    user1_data = user1_response.json()
    user1_id = user1_data["id"]
    assert user1_data["email"] == "user1@example.com"
    
    # Register second user
    user2_response = client.post(
        "/api/auth/register",
        json={
            "email": "user2@example.com",
            "password": "securepassword123"
        }
    )
    assert user2_response.status_code == 200
    user2_data = user2_response.json()
    user2_id = user2_data["id"]
    assert user2_data["email"] == "user2@example.com"
    
    # Login as user1 to get token
    login1_response = client.post(
        "/api/auth/login",
        data={
            "email": "user1@example.com",
            "password": "securepassword123"
        }
    )
    assert login1_response.status_code == 200
    token1 = login1_response.json()["access_token"]
    
    # Login as user2 to get token
    login2_response = client.post(
        "/api/auth/login",
        data={
            "email": "user2@example.com",
            "password": "securepassword123"
        }
    )
    assert login2_response.status_code == 200
    token2 = login2_response.json()["access_token"]
    
    # User1 should be able to access their own data
    headers1 = {"Authorization": f"Bearer {token1}"}
    user1_own_data = client.get(f"/api/users/{user1_id}", headers=headers1)
    assert user1_own_data.status_code == 200
    
    # User2 should be able to access their own data
    headers2 = {"Authorization": f"Bearer {token2}"}
    user2_own_data = client.get(f"/api/users/{user2_id}", headers=headers2)
    assert user2_own_data.status_code == 200
    
    # User1 should NOT be able to access User2's data using User1's token but User2's ID
    malicious_request = client.get(f"/api/users/{user2_id}", headers=headers1)
    assert malicious_request.status_code == 403  # Forbidden
    
    # User2 should NOT be able to access User1's data using User2's token but User1's ID
    malicious_request2 = client.get(f"/api/users/{user1_id}", headers=headers2)
    assert malicious_request2.status_code == 403  # Forbidden