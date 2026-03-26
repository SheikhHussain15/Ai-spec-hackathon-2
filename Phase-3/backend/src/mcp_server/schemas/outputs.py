"""
MCP Tool Output Schemas.

Standardized output response formats for all tools.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class TaskOutput(BaseModel):
    """Task data in tool responses."""
    id: str
    title: str
    description: Optional[str] = None
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class ListTasksOutput(BaseModel):
    """Output schema for list_tasks tool."""
    tasks: List[TaskOutput]
    count: int


class DeleteConfirmationOutput(BaseModel):
    """Output schema for delete_task tool."""
    deleted: bool
    task_id: str


class ValidationErrorDetails(BaseModel):
    """Validation error details."""
    field: str
    reason: str
    received: Any


class OwnershipViolationDetails(BaseModel):
    """Ownership violation error details."""
    requested_resource_id: str
    authenticated_user_id: str


class NotFoundDetails(BaseModel):
    """Not found error details."""
    resource_type: str
    resource_id: str


__all__ = [
    "TaskOutput",
    "ListTasksOutput",
    "DeleteConfirmationOutput",
    "ValidationErrorDetails",
    "OwnershipViolationDetails",
    "NotFoundDetails",
]
