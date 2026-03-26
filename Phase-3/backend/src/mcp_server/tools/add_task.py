"""
add_task MCP Tool Handler.

Creates a new task for the authenticated user.
"""

import time
from datetime import datetime
from sqlmodel import Session
from src.mcp_server.utils.db import get_session
from src.mcp_server.utils.logging import log_tool_invocation
from src.mcp_server.utils.errors import ValidationError, DatabaseError
from src.models.task import Task


async def add_task(user_id: str, title: str, description: str = None) -> dict:
    """
    Add a new task for the authenticated user.
    
    Args:
        user_id: Authenticated user ID
        title: Task title
        description: Optional task description
        
    Returns:
        Success response with created task data
    """
    start_time = time.time()
    tool_name = "add_task"
    
    try:
        # Validate inputs
        if not title or not title.strip():
            raise ValidationError(
                field="title",
                reason="Title is required",
                received=title,
                tool_name=tool_name
            )
        
        session = get_session()
        try:
            # Create task
            task = Task(
                title=title.strip(),
                description=description.strip() if description else None,
                user_id=user_id,
                completed=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            session.add(task)
            session.commit()
            session.refresh(task)

            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)

            # Log successful invocation
            log_tool_invocation(
                user_id=user_id,
                tool_name=tool_name,
                inputs={"title": title, "description": description},
                success=True,
                execution_time_ms=execution_time_ms
            )

            # Return success response
            return {
                "success": True,
                "data": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "user_id": task.user_id,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
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
            inputs={"title": title, "description": description},
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
            inputs={"title": title, "description": description},
            success=False,
            execution_time_ms=execution_time_ms,
            error=f"Database error: {str(e)}"
        )
        return DatabaseError(
            operation="INSERT",
            error_summary=str(e),
            tool_name=tool_name
        ).to_response(tool_name)
