import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch

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

def test_create_task():
    """Test creating a new task"""
    # Mock a valid token
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': 'test-user-id'})()
        
        response = client.post(
            "/api/tasks/test-user-id/tasks",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "completed": False
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test Description"
        assert data["completed"] is False
        assert data["user_id"] == "test-user-id"


def test_get_user_tasks():
    """Test getting all tasks for a user"""
    # Mock a valid token
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': 'test-user-id'})()
        
        # First create a task
        client.post(
            "/api/tasks/test-user-id/tasks",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "completed": False
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        response = client.get("/api/tasks/test-user-id/tasks", headers={"Authorization": "Bearer fake-token"})
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Task"


def test_get_specific_task():
    """Test getting a specific task"""
    # Mock a valid token
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': 'test-user-id'})()
        
        # First create a task
        create_response = client.post(
            "/api/tasks/test-user-id/tasks",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "completed": False
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        task_id = create_response.json()["id"]
        
        response = client.get(f"/api/tasks/test-user-id/tasks/{task_id}", headers={"Authorization": "Bearer fake-token"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Task"


def test_update_task():
    """Test updating a task"""
    # Mock a valid token
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': 'test-user-id'})()
        
        # First create a task
        create_response = client.post(
            "/api/tasks/test-user-id/tasks",
            json={
                "title": "Original Task",
                "description": "Original Description",
                "completed": False
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        task_id = create_response.json()["id"]
        
        response = client.put(
            f"/api/tasks/test-user-id/tasks/{task_id}",
            json={
                "title": "Updated Task",
                "description": "Updated Description",
                "completed": True
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Task"
        assert data["completed"] is True


def test_patch_task_completion():
    """Test updating only the completion status of a task"""
    # Mock a valid token
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': 'test-user-id'})()
        
        # First create a task
        create_response = client.post(
            "/api/tasks/test-user-id/tasks",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "completed": False
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        task_id = create_response.json()["id"]
        
        response = client.patch(
            f"/api/tasks/test-user-id/tasks/{task_id}/complete",
            json={
                "completed": True
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True


def test_delete_task():
    """Test deleting a task"""
    # Mock a valid token
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': 'test-user-id'})()
        
        # First create a task
        create_response = client.post(
            "/api/tasks/test-user-id/tasks",
            json={
                "title": "Test Task to Delete",
                "description": "Test Description",
                "completed": False
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        task_id = create_response.json()["id"]
        
        response = client.delete(f"/api/tasks/test-user-id/tasks/{task_id}", headers={"Authorization": "Bearer fake-token"})
        
        assert response.status_code == 204
        
        # Verify the task is gone
        get_response = client.get(f"/api/tasks/test-user-id/tasks/{task_id}", headers={"Authorization": "Bearer fake-token"})
        assert get_response.status_code == 404