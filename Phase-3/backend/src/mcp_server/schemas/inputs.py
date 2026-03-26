"""
MCP Tool Input Validation Schemas.

All input schemas use Pydantic for strict validation.
"""

from pydantic import BaseModel, Field
from typing import Optional


class AddTaskInput(BaseModel):
    """Input schema for add_task tool."""
    user_id: str = Field(..., description="Authenticated user ID (UUID format)")
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Optional task description")


class ListTasksInput(BaseModel):
    """Input schema for list_tasks tool."""
    user_id: str = Field(..., description="Authenticated user ID (UUID format)")
    completed: Optional[bool] = Field(None, description="Filter by completion status")


class CompleteTaskInput(BaseModel):
    """Input schema for complete_task tool."""
    user_id: str = Field(..., description="Authenticated user ID (UUID format)")
    task_id: str = Field(..., description="Task ID to complete (UUID format)")


class DeleteTaskInput(BaseModel):
    """Input schema for delete_task tool."""
    user_id: str = Field(..., description="Authenticated user ID (UUID format)")
    task_id: str = Field(..., description="Task ID to delete (UUID format)")


class UpdateTaskInput(BaseModel):
    """Input schema for update_task tool."""
    user_id: str = Field(..., description="Authenticated user ID (UUID format)")
    task_id: str = Field(..., description="Task ID to update (UUID format)")
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="New task title")
    description: Optional[str] = Field(None, max_length=1000, description="New task description")
    completed: Optional[bool] = Field(None, description="New completion status")


__all__ = [
    "AddTaskInput",
    "ListTasksInput",
    "CompleteTaskInput",
    "DeleteTaskInput",
    "UpdateTaskInput",
]
