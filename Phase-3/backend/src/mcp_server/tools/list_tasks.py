"""
list_tasks MCP Tool Handler.

Lists all tasks for the authenticated user.
"""

import time
from sqlmodel import select
from src.mcp_server.utils.db import get_session
from src.mcp_server.utils.logging import log_tool_invocation
from src.mcp_server.utils.errors import ValidationError
from src.models.task import Task


async def list_tasks(user_id: str, completed: bool = None) -> dict:
    """
    List all tasks for the authenticated user.
    
    Args:
        user_id: Authenticated user ID
        completed: Optional filter by completion status
        
    Returns:
        Success response with array of tasks
    """
    start_time = time.time()
    tool_name = "list_tasks"
    
    try:
        session = get_session()
        try:
            # Build query with user isolation
            statement = select(Task).where(Task.user_id == user_id)
            
            # Apply completion filter if provided
            if completed is not None:
                statement = statement.where(Task.completed == completed)
            
            # Order by created_at descending (newest first)
            statement = statement.order_by(Task.created_at.desc())
            
            # Execute query
            results = session.exec(statement)
            tasks = list(results.all())
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Log successful invocation
            log_tool_invocation(
                user_id=user_id,
                tool_name=tool_name,
                inputs={"user_id": user_id, "completed": completed},
                success=True,
                execution_time_ms=execution_time_ms
            )
            
            # Return success response
            return {
                "success": True,
                "data": {
                    "tasks": [
                        {
                            "id": task.id,
                            "title": task.title,
                            "description": task.description,
                            "user_id": task.user_id,
                            "completed": task.completed,
                            "created_at": task.created_at.isoformat(),
                            "updated_at": task.updated_at.isoformat()
                        }
                        for task in tasks
                    ],
                    "count": len(tasks)
                },
                "tool_name": tool_name,
                "execution_time_ms": execution_time_ms
            }
        finally:
            session.close()
            
    except ValidationError as e:
        execution_time_ms = int((time.time() - start_time) * 1000)
        log_tool_invocation(
            user_id=user_id,
            tool_name=tool_name,
            inputs={"user_id": user_id, "completed": completed},
            success=False,
            execution_time_ms=execution_time_ms,
            error=str(e)
        )
        return e.to_response(tool_name)
        
    except Exception as e:
        execution_time_ms = int((time.time() - start_time) * 1000)
        log_tool_invocation(
            user_id=user_id,
            tool_name=tool_name,
            inputs={"user_id": user_id, "completed": completed},
            success=False,
            execution_time_ms=execution_time_ms,
            error=f"Database error: {str(e)}"
        )
        from src.mcp_server.utils.errors import DatabaseError
        return DatabaseError(
            operation="SELECT",
            error_summary=str(e),
            tool_name=tool_name
        ).to_response(tool_name)
