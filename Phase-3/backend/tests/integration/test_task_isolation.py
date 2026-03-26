import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch
import uuid

from src.main import app
from src.database import get_session
from src.models.task import Task

# Create a test database engine
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create the tables in the test database
SQLModel.metadata.create_all(bind=test_engine)

def override_get_session():
    with Session(test_engine) as session:
        yield session

# Override the database session in the app
app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)

def test_user_isolation_integration():
    """
    Integration test for user isolation - ensure users can't access other users' tasks
    """
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())
    
    # Mock a valid token for user1
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': user1_id})()
        
        # Create a task for user1
        create_response = client.post(
            f"/api/tasks/{user1_id}/tasks",
            json={
                "title": "User1's Task",
                "description": "This belongs to user1",
                "completed": False
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        assert create_response.status_code == 200
        user1_task = create_response.json()
        task_id = user1_task["id"]
        
        # Now switch to user2's context
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': user2_id})()
        
        # User2 should NOT be able to access user1's task
        get_response = client.get(f"/api/tasks/{user1_id}/tasks/{task_id}", headers={"Authorization": "Bearer fake-token"})
        assert get_response.status_code == 403  # Forbidden
        
        # User2 should NOT be able to update user1's task
        update_response = client.put(
            f"/api/tasks/{user1_id}/tasks/{task_id}",
            json={
                "title": "Hacked Task",
                "description": "Hacker's description",
                "completed": True
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        assert update_response.status_code == 403  # Forbidden
        
        # User2 should NOT be able to delete user1's task
        delete_response = client.delete(f"/api/tasks/{user1_id}/tasks/{task_id}", headers={"Authorization": "Bearer fake-token"})
        assert delete_response.status_code == 403  # Forbidden
        
        # User2 should NOT be able to patch user1's task
        patch_response = client.patch(
            f"/api/tasks/{user1_id}/tasks/{task_id}/complete",
            json={"completed": True},
            headers={"Authorization": "Bearer fake-token"}
        )
        assert patch_response.status_code == 403  # Forbidden
        
        # User2 should be able to access their own tasks
        # First create a task for user2
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': user2_id})()
        user2_create_response = client.post(
            f"/api/tasks/{user2_id}/tasks",
            json={
                "title": "User2's Task",
                "description": "This belongs to user2",
                "completed": False
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        assert user2_create_response.status_code == 200
        user2_task = user2_create_response.json()
        user2_task_id = user2_task["id"]
        
        # User2 should be able to access their own task
        user2_get_response = client.get(f"/api/tasks/{user2_id}/tasks/{user2_task_id}", headers={"Authorization": "Bearer fake-token"})
        assert user2_get_response.status_code == 200