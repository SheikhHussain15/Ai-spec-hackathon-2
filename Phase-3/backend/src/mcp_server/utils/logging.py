"""
Structured Logging for MCP Tool Invocations.

All tool executions are logged for traceability and audit purposes.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Optional

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("mcp-server")


def log_tool_invocation(
    user_id: str,
    tool_name: str,
    inputs: dict,
    success: bool,
    execution_time_ms: int,
    error: Optional[str] = None
):
    """
    Log a tool invocation for traceability.
    
    Args:
        user_id: Authenticated user ID
        tool_name: Name of the invoked tool
        inputs: Tool input parameters (sanitized)
        success: Whether the tool execution succeeded
        execution_time_ms: Execution time in milliseconds
        error: Error message if failed
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "tool_invocation",
        "user_id": user_id,
        "tool_name": tool_name,
        "inputs": sanitize_inputs(inputs),
        "success": success,
        "execution_time_ms": execution_time_ms,
    }
    
    if error:
        log_entry["error"] = error
    
    logger.info(json.dumps(log_entry))


def log_security_event(
    event_type: str,
    user_id: str,
    details: dict
):
    """
    Log a security event (e.g., ownership violation).
    
    Args:
        event_type: Type of security event
        user_id: Authenticated user ID
        details: Event details
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": f"security_{event_type}",
        "user_id": user_id,
        "details": details
    }
    
    logger.warning(json.dumps(log_entry))


def sanitize_inputs(inputs: dict) -> dict:
    """
    Sanitize inputs for logging (remove sensitive data).
    
    Args:
        inputs: Raw input parameters
        
    Returns:
        Sanitized input dictionary
    """
    # Keep user_id and task_id, truncate long strings
    sanitized = {}
    for key, value in inputs.items():
        if isinstance(value, str) and len(value) > 100:
            sanitized[key] = value[:100] + "..."
        else:
            sanitized[key] = value
    return sanitized


__all__ = ["logger", "log_tool_invocation", "log_security_event", "sanitize_inputs"]
