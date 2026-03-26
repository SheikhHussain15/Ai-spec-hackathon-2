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

def test_complete_task_lifecycle():
    """Integration test for the complete task lifecycle"""
    user_id = str(uuid.uuid4())
    
    # Mock a valid token for this user
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': user_id})()
        
        # 1. Create a task
        create_response = client.post(
            f"/api/tasks/{user_id}/tasks",
            json={
                "title": "Integration Test Task",
                "description": "This is a test task for integration testing",
                "completed": False
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        assert create_response.status_code == 200
        created_task = create_response.json()
        task_id = created_task["id"]
        
        assert created_task["title"] == "Integration Test Task"
        assert created_task["description"] == "This is a test task for integration testing"
        assert created_task["completed"] is False
        assert created_task["user_id"] == user_id
        
        # 2. Get the specific task
        get_one_response = client.get(f"/api/tasks/{user_id}/tasks/{task_id}", headers={"Authorization": "Bearer fake-token"})
        assert get_one_response.status_code == 200
        retrieved_task = get_one_response.json()
        assert retrieved_task["id"] == task_id
        assert retrieved_task["title"] == "Integration Test Task"
        
        # 3. Get all tasks for the user
        get_all_response = client.get(f"/api/tasks/{user_id}/tasks", headers={"Authorization": "Bearer fake-token"})
        assert get_all_response.status_code == 200
        tasks_list = get_all_response.json()
        assert len(tasks_list) == 1
        assert tasks_list[0]["id"] == task_id
        
        # 4. Update the task
        update_response = client.put(
            f"/api/tasks/{user_id}/tasks/{task_id}",
            json={
                "title": "Updated Integration Test Task",
                "description": "Updated description for integration testing",
                "completed": True
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        assert update_response.status_code == 200
        updated_task = update_response.json()
        assert updated_task["title"] == "Updated Integration Test Task"
        assert updated_task["completed"] is True
        
        # 5. Toggle completion status separately
        patch_response = client.patch(
            f"/api/tasks/{user_id}/tasks/{task_id}/complete",
            json={"completed": False},
            headers={"Authorization": "Bearer fake-token"}
        )
        
        assert patch_response.status_code == 200
        patched_task = patch_response.json()
        assert patched_task["completed"] is False
        
        # 6. Delete the task
        delete_response = client.delete(f"/api/tasks/{user_id}/tasks/{task_id}", headers={"Authorization": "Bearer fake-token"})
        assert delete_response.status_code == 204
        
        # 7. Verify the task is deleted
        verify_delete_response = client.get(f"/api/tasks/{user_id}/tasks/{task_id}", headers={"Authorization": "Bearer fake-token"})
        assert verify_delete_response.status_code == 404


def test_user_isolation():
    """Integration test to ensure users can't access each other's tasks"""
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
        
        # Now switch to user2's token
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