"""
update_task MCP Tool Handler.

Updates a specific task's fields.
"""

import time
from datetime import datetime
from sqlmodel import select
from src.mcp_server.utils.db import get_session
from src.mcp_server.utils.logging import log_tool_invocation, log_security_event
from src.mcp_server.utils.errors import ValidationError, NotFoundError, OwnershipViolationError
from src.models.task import Task


async def update_task(
    user_id: str,
    task_id: str,
    title: str = None,
    description: str = None,
    completed: bool = None
) -> dict:
    """
    Update a specific task's fields.
    
    Args:
        user_id: Authenticated user ID
        task_id: Task ID to update
        title: Optional new task title
        description: Optional new task description
        completed: Optional new completion status
        
    Returns:
        Success response with updated task data
    """
    start_time = time.time()
    tool_name = "update_task"
    
    try:
        session = get_session()
        try:
            # Query for the task
            statement = select(Task).where(Task.id == task_id)
            result = session.exec(statement).first()
            
            if not result:
                execution_time_ms = int((time.time() - start_time) * 1000)
                return NotFoundError(
                    resource_type="Task",
                    resource_id=task_id,
                    tool_name=tool_name
                ).to_response(tool_name)
            
            task = result
            
            # Check ownership
            if task.user_id != user_id:
                execution_time_ms = int((time.time() - start_time) * 1000)
                
                # Log security event
                log_security_event(
                    event_type="ownership_violation",
                    user_id=user_id,
                    details={
                        "task_id": task_id,
                        "task_owner_id": task.user_id
                    }
                )
                
                return OwnershipViolationError(
                    resource_id=task_id,
                    user_id=user_id,
                    tool_name=tool_name
                ).to_response(tool_name)
            
            # Update task fields (only provided fields)
            if title is not None:
                task.title = title.strip()
            if description is not None:
                task.description = description.strip() if description else None
            if completed is not None:
                task.completed = completed
            
            task.updated_at = datetime.utcnow()
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Log successful invocation
            log_tool_invocation(
                user_id=user_id,
                tool_name=tool_name,
                inputs={
                    "user_id": user_id,
                    "task_id": task_id,
                    "title": title,
                    "description": description,
                    "completed": completed
                },
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
            inputs={
                "user_id": user_id,
                "task_id": task_id,
                "title": title,
                "description": description,
                "completed": completed
            },
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
            inputs={
                "user_id": user_id,
                "task_id": task_id,
                "title": title,
                "description": description,
                "completed": completed
            },
            success=False,
            execution_time_ms=execution_time_ms,
            error=f"Database error: {str(e)}"
        )
        from src.mcp_server.utils.errors import DatabaseError
        return DatabaseError(
            operation="UPDATE",
            error_summary=str(e),
            tool_name=tool_name
        ).to_response(tool_name)
