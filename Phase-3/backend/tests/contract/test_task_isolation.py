import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch

client = TestClient(app)

def test_user_isolation_contract():
    """
    Contract test for user isolation - ensure users can't access other users' tasks
    """
    # Mock a valid token for user1
    with patch("src.middleware.auth_middleware.get_current_user") as mock_get_current_user:
        mock_get_current_user.return_value = type('MockTokenData', (), {'user_id': 'user1-id'})()
        
        # Try to access user2's tasks with user1's token
        response = client.get("/api/tasks/user2-id/tasks", headers={"Authorization": "Bearer fake-token"})
        
        # Should return 403 Forbidden due to user ID mismatch
        assert response.status_code == 403
        
        # Try to access a specific task belonging to user2 with user1's token
        response = client.get("/api/tasks/user2-id/tasks/some-task-id", headers={"Authorization": "Bearer fake-token"})
        
        # Should return 403 Forbidden due to user ID mismatch
        assert response.status_code == 403
        
        # Try to create a task for user2 with user1's token
        response = client.post(
            "/api/tasks/user2-id/tasks",
            json={
                "title": "Hacker's Task",
                "description": "Trying to create for another user",
                "completed": False
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        # Should return 403 Forbidden due to user ID mismatch
        assert response.status_code == 403
        
        # Try to update a task belonging to user2 with user1's token
        response = client.put(
            "/api/tasks/user2-id/tasks/some-task-id",
            json={
                "title": "Hacked Task",
                "description": "Hacker's description",
                "completed": True
            },
            headers={"Authorization": "Bearer fake-token"}
        )
        
        # Should return 403 Forbidden due to user ID mismatch
        assert response.status_code == 403
        
        # Try to delete a task belonging to user2 with user1's token
        response = client.delete("/api/tasks/user2-id/tasks/some-task-id", headers={"Authorization": "Bearer fake-token"})
        
        # Should return 403 Forbidden due to user ID mismatch
        assert response.status_code == 403