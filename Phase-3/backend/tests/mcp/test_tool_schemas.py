"""
MCP Tool Contract Tests.

Tests to verify MCP tool schemas and basic functionality.
"""

import pytest
from mcp_server.schemas.inputs import (
    AddTaskInput,
    ListTasksInput,
    CompleteTaskInput,
    DeleteTaskInput,
    UpdateTaskInput,
)


class TestAddTaskInput:
    """Test add_task input validation."""
    
    def test_valid_input(self):
        """Test valid add_task input."""
        input_data = AddTaskInput(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            title="Test Task",
            description="Test description"
        )
        assert input_data.title == "Test Task"
        assert input_data.description == "Test description"
    
    def test_title_required(self):
        """Test that title is required."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            AddTaskInput(
                user_id="550e8400-e29b-41d4-a716-446655440000",
                title=""
            )
    
    def test_title_max_length(self):
        """Test title max length validation."""
        with pytest.raises(Exception):
            AddTaskInput(
                user_id="550e8400-e29b-41d4-a716-446655440000",
                title="x" * 201
            )
    
    def test_description_max_length(self):
        """Test description max length validation."""
        with pytest.raises(Exception):
            AddTaskInput(
                user_id="550e8400-e29b-41d4-a716-446655440000",
                title="Test",
                description="x" * 1001
            )


class TestListTasksInput:
    """Test list_tasks input validation."""
    
    def test_valid_input_no_filter(self):
        """Test valid list_tasks input without filter."""
        input_data = ListTasksInput(
            user_id="550e8400-e29b-41d4-a716-446655440000"
        )
        assert input_data.user_id == "550e8400-e29b-41d4-a716-446655440000"
        assert input_data.completed is None
    
    def test_valid_input_with_filter(self):
        """Test valid list_tasks input with completion filter."""
        input_data = ListTasksInput(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            completed=True
        )
        assert input_data.completed is True


class TestCompleteTaskInput:
    """Test complete_task input validation."""
    
    def test_valid_input(self):
        """Test valid complete_task input."""
        input_data = CompleteTaskInput(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            task_id="task-uuid-here"
        )
        assert input_data.user_id == "550e8400-e29b-41d4-a716-446655440000"
        assert input_data.task_id == "task-uuid-here"


class TestDeleteTaskInput:
    """Test delete_task input validation."""
    
    def test_valid_input(self):
        """Test valid delete_task input."""
        input_data = DeleteTaskInput(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            task_id="task-uuid-here"
        )
        assert input_data.user_id == "550e8400-e29b-41d4-a716-446655440000"
        assert input_data.task_id == "task-uuid-here"


class TestUpdateTaskInput:
    """Test update_task input validation."""
    
    def test_valid_input_minimal(self):
        """Test valid update_task input with minimal fields."""
        input_data = UpdateTaskInput(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            task_id="task-uuid-here"
        )
        assert input_data.title is None
        assert input_data.description is None
        assert input_data.completed is None
    
    def test_valid_input_all_fields(self):
        """Test valid update_task input with all fields."""
        input_data = UpdateTaskInput(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            task_id="task-uuid-here",
            title="Updated Title",
            description="Updated description",
            completed=True
        )
        assert input_data.title == "Updated Title"
        assert input_data.completed is True
