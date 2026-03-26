"""
MCP Tool Schema Definitions.

This module defines shared schema types for MCP tool inputs and outputs.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class ToolSuccessResponse(BaseModel):
    """Standard success response for all MCP tools."""
    success: bool = True
    data: dict
    tool_name: str
    execution_time_ms: int


class ToolErrorResponse(BaseModel):
    """Standard error response for all MCP tools."""
    success: bool = False
    error: str
    error_code: str
    tool_name: str
    details: Optional[dict] = None


class TaskData(BaseModel):
    """Standard task data representation."""
    id: str
    title: str
    description: Optional[str] = None
    user_id: str
    completed: bool = False
    created_at: datetime
    updated_at: datetime


__all__ = [
    "ToolSuccessResponse",
    "ToolErrorResponse",
    "TaskData",
]
