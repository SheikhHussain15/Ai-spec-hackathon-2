"""
Tool Registry for MCP Server.

This module registers all MCP tools with the server instance.
"""


def register_all_tools(server):
    """
    Register all MCP tools with the server.
    
    Tools registered:
    - add_task: Create a new task
    - list_tasks: List all tasks for a user
    - complete_task: Mark a task as completed
    - delete_task: Delete a task
    - update_task: Update task fields
    """
    # Import tools to register them with the server
    # Lazy import to avoid circular dependencies during testing
    from src.mcp_server.tools import add_task, list_tasks, complete_task, delete_task, update_task
    
    # All tools are automatically registered via @server.tool() decorator
    # This function ensures all tool modules are imported
    pass


__all__ = ["register_all_tools"]
