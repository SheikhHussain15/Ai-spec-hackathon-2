"""
delete_task MCP Tool Handler.

Deletes a specific task.
"""

import time
from sqlmodel import select
from src.mcp_server.utils.db import get_session
from src.mcp_server.utils.logging import log_tool_invocation, log_security_event
from src.mcp_server.utils.errors import ValidationError, NotFoundError, OwnershipViolationError
from src.models.task import Task


async def delete_task(user_id: str, task_id: str) -> dict:
    """
    Delete a specific task.
    
    Args:
        user_id: Authenticated user ID
        task_id: Task ID to delete
        
    Returns:
        Success response with deletion confirmation
    """
    start_time = time.time()
    tool_name = "delete_task"
    
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
            
            # Delete task
            session.delete(task)
            session.commit()
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Log successful invocation
            log_tool_invocation(
                user_id=user_id,
                tool_name=tool_name,
                inputs={"user_id": user_id, "task_id": task_id},
                success=True,
                execution_time_ms=execution_time_ms
            )
            
            # Return success response
            return {
                "success": True,
                "data": {
                    "deleted": True,
                    "task_id": task_id
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
            inputs={"user_id": user_id, "task_id": task_id},
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
            inputs={"user_id": user_id, "task_id": task_id},
            success=False,
            execution_time_ms=execution_time_ms,
            error=f"Database error: {str(e)}"
        )
        from src.mcp_server.utils.errors import DatabaseError
        return DatabaseError(
            operation="DELETE",
            error_summary=str(e),
            tool_name=tool_name
        ).to_response(tool_name)
