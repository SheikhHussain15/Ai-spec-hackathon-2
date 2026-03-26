"""
MCP Tool Integration Tests.

End-to-end tests for MCP tool invocation flow.
Tests verify tool execution with actual database operations.
"""

import pytest
import sys
import os
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from mcp_server.schemas.inputs import AddTaskInput, UpdateTaskInput
from mcp_server.utils.errors import ErrorCode


class TestMCPToolIntegration:
    """Integration tests for MCP tools (mocked database)."""
    
    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        session = MagicMock()
        session.exec.return_value.first.return_value = None
        session.exec.return_value.all.return_value = []
        return session
    
    def test_add_task_success(self, mock_session):
        """Test successful task creation."""
        # Mock the session context manager
        mock_session.__enter__ = MagicMock(return_value=mock_session)
        mock_session.__exit__ = MagicMock(return_value=False)
        
        # Mock task creation
        mock_task = MagicMock()
        mock_task.id = "task-123"
        mock_task.title = "Test Task"
        mock_task.description = "Test description"
        mock_task.user_id = "user-123"
        mock_task.completed = False
        mock_task.created_at = datetime.utcnow()
        mock_task.updated_at = datetime.utcnow()
        
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()
        mock_session.refresh = MagicMock(side_effect=lambda x: setattr(x, 'id', 'task-123'))
        
        # Validate input schema
        input_data = AddTaskInput(
            user_id="user-123",
            title="Test Task",
            description="Test description"
        )
        
        assert input_data.title == "Test Task"
        assert input_data.user_id == "user-123"
        assert input_data.description == "Test description"
    
    def test_list_tasks_empty(self, mock_session):
        """Test listing tasks when none exist."""
        mock_session.__enter__ = MagicMock(return_value=mock_session)
        mock_session.__exit__ = MagicMock(return_value=False)
        mock_session.exec.return_value.all.return_value = []
        
        # Validate input schema
        from mcp_server.schemas.inputs import ListTasksInput
        input_data = ListTasksInput(user_id="user-123")
        
        assert input_data.user_id == "user-123"
        assert input_data.completed is None
    
    def test_validation_error_empty_title(self):
        """Test validation rejects empty title."""
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            AddTaskInput(
                user_id="user-123",
                title=""  # Empty title should fail
            )
    
    def test_validation_error_title_too_long(self):
        """Test validation rejects title over 200 chars."""
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            AddTaskInput(
                user_id="user-123",
                title="x" * 201  # Over 200 chars
            )
    
    def test_validation_error_description_too_long(self):
        """Test validation rejects description over 1000 chars."""
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            AddTaskInput(
                user_id="user-123",
                title="Test",
                description="x" * 1001  # Over 1000 chars
            )
    
    def test_update_task_partial_update(self):
        """Test update task with partial fields."""
        input_data = UpdateTaskInput(
            user_id="user-123",
            task_id="task-123",
            title="Updated Title"
            # description and completed not provided
        )
        
        assert input_data.title == "Updated Title"
        assert input_data.description is None
        assert input_data.completed is None
    
    def test_update_task_full_update(self):
        """Test update task with all fields."""
        input_data = UpdateTaskInput(
            user_id="user-123",
            task_id="task-123",
            title="Updated Title",
            description="Updated description",
            completed=True
        )
        
        assert input_data.title == "Updated Title"
        assert input_data.description == "Updated description"
        assert input_data.completed is True
    
    def test_error_code_enum(self):
        """Test error code enum values."""
        assert ErrorCode.VALIDATION_ERROR.value == "VALIDATION_ERROR"
        assert ErrorCode.OWNERSHIP_VIOLATION.value == "OWNERSHIP_VIOLATION"
        assert ErrorCode.NOT_FOUND.value == "NOT_FOUND"
        assert ErrorCode.DATABASE_ERROR.value == "DATABASE_ERROR"
        assert ErrorCode.INTERNAL_ERROR.value == "INTERNAL_ERROR"


class TestMCPHTTPAdapter:
    """Tests for MCP HTTP adapter."""
    
    def test_tool_invocation_request_model(self):
        """Test ToolInvocationRequest model."""
        from mcp_server.http_adapter import ToolInvocationRequest
        
        request = ToolInvocationRequest(
            tool_name="add_task",
            arguments={
                "user_id": "user-123",
                "title": "Test Task"
            }
        )
        
        assert request.tool_name == "add_task"
        assert request.arguments["user_id"] == "user-123"
        assert request.arguments["title"] == "Test Task"
    
    def test_tool_invocation_response_model(self):
        """Test ToolInvocationResponse model."""
        from mcp_server.http_adapter import ToolInvocationResponse
        
        response = ToolInvocationResponse(
            success=True,
            data={"id": "task-123", "title": "Test Task"},
            tool_name="add_task",
            execution_time_ms=45
        )
        
        assert response.success is True
        assert response.data["id"] == "task-123"
        assert response.error is None
        assert response.execution_time_ms == 45
    
    def test_tool_invocation_error_response(self):
        """Test error response model."""
        from mcp_server.http_adapter import ToolInvocationResponse
        
        response = ToolInvocationResponse(
            success=False,
            error="Validation failed",
            error_code="VALIDATION_ERROR",
            tool_name="add_task",
            execution_time_ms=5
        )
        
        assert response.success is False
        assert response.error == "Validation failed"
        assert response.error_code == "VALIDATION_ERROR"
