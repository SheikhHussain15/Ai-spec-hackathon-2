import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch
from datetime import datetime, timedelta
import time

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

def test_timestamp_accuracy_integration():
    """
    Integration test for timestamp accuracy in task operations
    """
    user_id = "test-user-id"
    
    # Mock a valid token
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': user_id})()
        
        # Record the time before creating the task
        before_creation = datetime.utcnow()
        time.sleep(0.01)  # Small delay to ensure time difference
        
        # Create a task
        create_response = client.post(
            f"/api/tasks/{user_id}/tasks",
            json={
                "title": "Timestamp Accuracy Test Task",
                "description": "Testing timestamp accuracy",
                "completed": False
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        # Record the time after creating the task
        after_creation = datetime.utcnow()
        
        assert create_response.status_code == 200
        created_task = create_response.json()
        
        # Parse the created_at timestamp from the response
        created_at_str = created_task["created_at"]
        created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00")).replace(tzinfo=None)
        
        # The created_at time should be between before_creation and after_creation
        assert before_creation <= created_at <= after_creation
        
        # Wait a bit before updating
        time.sleep(0.01)
        before_update = datetime.utcnow()
        time.sleep(0.01)
        
        # Update the task
        task_id = created_task["id"]
        update_response = client.put(
            f"/api/tasks/{user_id}/tasks/{task_id}",
            json={
                "title": "Updated Timestamp Accuracy Test Task",
                "description": "Updated timestamp accuracy test",
                "completed": True
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        after_update = datetime.utcnow()
        
        assert update_response.status_code == 200
        updated_task = update_response.json()
        
        # Parse the updated_at timestamp from the response
        updated_at_str = updated_task["updated_at"]
        updated_at = datetime.fromisoformat(updated_at_str.replace("Z", "+00:00")).replace(tzinfo=None)
        
        # The updated_at time should be between before_update and after_update
        assert before_update <= updated_at <= after_update
        
        # The updated_at should be later than created_at
        assert updated_at > created_at
        
        # Wait before patching
        time.sleep(0.01)
        before_patch = datetime.utcnow()
        time.sleep(0.01)
        
        # Patch the task completion status
        patch_response = client.patch(
            f"/api/tasks/{user_id}/tasks/{task_id}/complete",
            json={"completed": False},
            headers={"Authorization": "Bearer fake-token"}
        )
        
        after_patch = datetime.utcnow()
        
        assert patch_response.status_code == 200
        patched_task = patch_response.json()
        
        # Parse the updated_at timestamp from the response after patch
        patched_updated_at_str = patched_task["updated_at"]
        patched_updated_at = datetime.fromisoformat(patched_updated_at_str.replace("Z", "+00:00")).replace(tzinfo=None)
        
        # The updated_at time after patch should be between before_patch and after_patch
        assert before_patch <= patched_updated_at <= after_patch
        
        # The updated_at should be later than the previous updated_at
        assert patched_updated_at > updated_at