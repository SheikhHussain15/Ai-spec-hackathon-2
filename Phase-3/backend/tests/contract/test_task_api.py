import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch

client = TestClient(app)

def test_get_user_tasks_contract():
    """
    Contract test for GET /api/tasks/{user_id}/tasks endpoint
    """
    # Mock a valid token
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': 'test-user-id'})()
        
        response = client.get("/api/tasks/test-user-id/tasks", headers={"Authorization": "Bearer fake-token"})
        
        # Should return 200 OK with an array of tasks (could be empty)
        assert response.status_code in [200]  # Either 200 for success or 401/403 for auth issues


def test_post_user_task_contract():
    """
    Contract test for POST /api/tasks/{user_id}/tasks endpoint
    """
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
        
        # Should return 200 OK with the created task or 422 for validation errors
        assert response.status_code in [200, 422]


def test_put_user_task_contract():
    """
    Contract test for PUT /api/tasks/{user_id}/tasks/{id} endpoint
    """
    # Mock a valid token
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': 'test-user-id'})()
        
        response = client.put(
            "/api/tasks/test-user-id/tasks/nonexistent-task-id",
            json={
                "title": "Updated Task",
                "description": "Updated Description",
                "completed": True
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        # Should return 404 for non-existent task or 422 for validation errors
        assert response.status_code in [404, 422]


def test_delete_user_task_contract():
    """
    Contract test for DELETE /api/tasks/{user_id}/tasks/{id} endpoint
    """
    # Mock a valid token
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': 'test-user-id'})()
        
        response = client.delete("/api/tasks/test-user-id/tasks/nonexistent-task-id", headers={"Authorization": "Bearer fake-token"})
        
        # Should return 404 for non-existent task
        assert response.status_code == 404