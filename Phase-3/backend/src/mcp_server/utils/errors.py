"""
Error Taxonomy for MCP Tools.

Standardized error codes and response formatting.
"""

from enum import Enum
from typing import Optional, Any


class ErrorCode(str, Enum):
    """Standard error codes for all MCP tools."""
    
    VALIDATION_ERROR = "VALIDATION_ERROR"
    OWNERSHIP_VIOLATION = "OWNERSHIP_VIOLATION"
    NOT_FOUND = "NOT_FOUND"
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class MCPError(Exception):
    """Base exception for MCP tool errors."""
    
    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        details: Optional[dict] = None
    ):
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        super().__init__(message)
    
    def to_response(self, tool_name: str) -> dict:
        """Convert to error response dictionary."""
        return {
            "success": False,
            "error": self.message,
            "error_code": self.error_code.value,
            "tool_name": tool_name,
            "details": self.details
        }


class ValidationError(MCPError):
    """Raised when input validation fails."""
    
    def __init__(
        self,
        field: str,
        reason: str,
        received: Any,
        tool_name: str
    ):
        super().__init__(
            error_code=ErrorCode.VALIDATION_ERROR,
            message=f"Input validation failed: {field} - {reason}",
            details={
                "field": field,
                "reason": reason,
                "received": received
            }
        )


class OwnershipViolationError(MCPError):
    """Raised when user attempts to access another user's resource."""
    
    def __init__(
        self,
        resource_id: str,
        user_id: str,
        tool_name: str
    ):
        super().__init__(
            error_code=ErrorCode.OWNERSHIP_VIOLATION,
            message="Access denied: You do not own this resource",
            details={
                "requested_resource_id": resource_id,
                "authenticated_user_id": user_id
            }
        )


class NotFoundError(MCPError):
    """Raised when a resource is not found."""
    
    def __init__(
        self,
        resource_type: str,
        resource_id: str,
        tool_name: str
    ):
        super().__init__(
            error_code=ErrorCode.NOT_FOUND,
            message=f"Resource not found: {resource_type} with ID {resource_id}",
            details={
                "resource_type": resource_type,
                "resource_id": resource_id
            }
        )


class DatabaseError(MCPError):
    """Raised when a database operation fails."""
    
    def __init__(
        self,
        operation: str,
        error_summary: str,
        tool_name: str
    ):
        super().__init__(
            error_code=ErrorCode.DATABASE_ERROR,
            message=f"Database operation failed: {error_summary}",
            details={
                "operation": operation,
                "error_summary": error_summary
            }
        )


class InternalError(MCPError):
    """Raised for unexpected internal errors."""
    
    def __init__(
        self,
        trace_id: str,
        tool_name: str
    ):
        super().__init__(
            error_code=ErrorCode.INTERNAL_ERROR,
            message="An unexpected error occurred. Please try again.",
            details={
                "trace_id": trace_id
            }
        )


def create_error_response(
    error_code: ErrorCode,
    message: str,
    tool_name: str,
    details: Optional[dict] = None
) -> dict:
    """
    Create a standardized error response.
    
    Args:
        error_code: Error code from ErrorCode enum
        message: Human-readable error message
        tool_name: Name of the tool that encountered the error
        details: Additional error context
        
    Returns:
        Standardized error response dictionary
    """
    return {
        "success": False,
        "error": message,
        "error_code": error_code.value,
        "tool_name": tool_name,
        "details": details or {}
    }


__all__ = [
    "ErrorCode",
    "MCPError",
    "ValidationError",
    "OwnershipViolationError",
    "NotFoundError",
    "DatabaseError",
    "InternalError",
    "create_error_response",
]
