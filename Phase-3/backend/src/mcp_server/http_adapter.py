"""
MCP HTTP Adapter for FastAPI.

This module provides HTTP endpoints for MCP tool invocation, enabling serverless deployment.
"""

from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/mcp", tags=["MCP Tools"])


class ToolInvocationRequest(BaseModel):
    """Request model for tool invocation."""
    tool_name: str
    arguments: dict


class ToolInvocationResponse(BaseModel):
    """Response model for tool invocation."""
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    tool_name: str
    execution_time_ms: int


@router.post("/invoke", response_model=ToolInvocationResponse)
async def invoke_tool(
    request: ToolInvocationRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
):
    """
    Invoke an MCP tool via HTTP.
    
    This endpoint allows AI agents to invoke MCP tools through HTTP POST requests,
    enabling serverless deployment scenarios.
    
    Args:
        request: Tool invocation request with tool name and arguments
        x_user_id: Authenticated user ID from JWT (optional, can be in arguments)
    
    Returns:
        Tool execution result
    """
    # Extract user_id from header or arguments
    user_id = x_user_id or request.arguments.get("user_id")
    
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="user_id required in X-User-Id header or arguments"
        )
    
    # Lazy import of tool handlers to avoid circular imports
    from src.mcp_server.tools.add_task import add_task
    from src.mcp_server.tools.list_tasks import list_tasks
    from src.mcp_server.tools.complete_task import complete_task
    from src.mcp_server.tools.delete_task import delete_task
    from src.mcp_server.tools.update_task import update_task
    
    try:
        # Route to appropriate tool handler
        if request.tool_name == "add_task":
            result = await add_task(**request.arguments)
        elif request.tool_name == "list_tasks":
            result = await list_tasks(**request.arguments)
        elif request.tool_name == "complete_task":
            result = await complete_task(**request.arguments)
        elif request.tool_name == "delete_task":
            result = await delete_task(**request.arguments)
        elif request.tool_name == "update_task":
            result = await update_task(**request.arguments)
        else:
            return ToolInvocationResponse(
                success=False,
                error=f"Unknown tool: {request.tool_name}",
                error_code="NOT_FOUND",
                tool_name=request.tool_name,
                execution_time_ms=0
            )
        
        return ToolInvocationResponse(**result)
        
    except Exception as e:
        return ToolInvocationResponse(
            success=False,
            error=str(e),
            error_code="INTERNAL_ERROR",
            tool_name=request.tool_name,
            execution_time_ms=0
        )


@router.get("/tools")
async def list_available_tools():
    """
    List all available MCP tools.
    
    Returns metadata about available tools for AI agent discovery.
    """
    return {
        "tools": [
            {
                "name": "add_task",
                "description": "Add a new task for the authenticated user",
                "parameters": {
                    "user_id": {"type": "string", "required": True, "description": "User ID"},
                    "title": {"type": "string", "required": True, "description": "Task title"},
                    "description": {"type": "string", "required": False, "description": "Task description"}
                }
            },
            {
                "name": "list_tasks",
                "description": "List all tasks for the authenticated user",
                "parameters": {
                    "user_id": {"type": "string", "required": True, "description": "User ID"},
                    "completed": {"type": "boolean", "required": False, "description": "Filter by completion"}
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a specific task as completed",
                "parameters": {
                    "user_id": {"type": "string", "required": True, "description": "User ID"},
                    "task_id": {"type": "string", "required": True, "description": "Task ID"}
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a specific task",
                "parameters": {
                    "user_id": {"type": "string", "required": True, "description": "User ID"},
                    "task_id": {"type": "string", "required": True, "description": "Task ID"}
                }
            },
            {
                "name": "update_task",
                "description": "Update a specific task's fields",
                "parameters": {
                    "user_id": {"type": "string", "required": True, "description": "User ID"},
                    "task_id": {"type": "string", "required": True, "description": "Task ID"},
                    "title": {"type": "string", "required": False, "description": "New title"},
                    "description": {"type": "string", "required": False, "description": "New description"},
                    "completed": {"type": "boolean", "required": False, "description": "Completion status"}
                }
            }
        ]
    }
