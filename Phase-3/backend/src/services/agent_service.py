"""
Agent Service for AI chat orchestration.

Supports multiple AI providers:
- Google AI Studio (Gemini)
- Rule-based fallback (no API key required)
"""

import os
import time
import json
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AI Provider configuration
AI_PROVIDER = os.getenv("AI_PROVIDER", "rule-based")  # Options: google, rule-based
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")

from src.agent.config import (
    agent_config,
    tool_config,
)

# Lazy import MCP tools to avoid circular dependencies
def _get_mcp_tools():
    """Lazy load MCP tools to avoid import issues."""
    try:
        from src.mcp_server.tools.add_task import add_task
        from src.mcp_server.tools.list_tasks import list_tasks
        from src.mcp_server.tools.complete_task import complete_task
        from src.mcp_server.tools.delete_task import delete_task
        from src.mcp_server.tools.update_task import update_task
        
        return {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "complete_task": complete_task,
            "delete_task": delete_task,
            "update_task": update_task,
        }
    except Exception as e:
        print(f"Warning: Could not load MCP tools: {e}")
        return {}


def get_mcp_tool_definitions() -> List[Dict[str, Any]]:
    """Get OpenAI function definitions for MCP tools (for compatibility)."""
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Task title (1-200 characters)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional task description (max 1000 characters)"
                        }
                    },
                    "required": ["title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List all tasks for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "completed": {
                            "type": "boolean",
                            "description": "Filter by completion status (optional)"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "Task ID to complete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "Task ID to delete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update task fields",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "Task ID to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New task title"
                        },
                        "description": {
                            "type": "string",
                            "description": "New task description"
                        },
                        "completed": {
                            "type": "boolean",
                            "description": "New completion status"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        }
    ]


async def execute_mcp_tool(
    tool_name: str,
    arguments: Dict[str, Any],
    user_id: str
) -> Dict[str, Any]:
    """
    Execute an MCP tool with error handling.

    Args:
        tool_name: Name of the tool to execute
        arguments: Tool arguments
        user_id: Authenticated user ID

    Returns:
        Tool execution result with success/error status
    """
    start_time = time.time()
    
    # Lazy load MCP tools
    mcp_tools = _get_mcp_tools()
    
    # Check if tools loaded
    if not mcp_tools:
        return {
            "success": False,
            "error": "MCP tools not loaded - check imports",
            "error_code": "TOOLS_NOT_AVAILABLE",
            "execution_time_ms": 0
        }

    if tool_name not in mcp_tools:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}. Available: {list(mcp_tools.keys())}",
            "error_code": "NOT_FOUND",
            "execution_time_ms": 0
        }

    try:
        tool_func = mcp_tools[tool_name]
        # Add user_id to arguments if not present
        if "user_id" not in arguments:
            arguments["user_id"] = user_id

        # Execute tool
        result = await tool_func(**arguments)

        execution_time_ms = int((time.time() - start_time) * 1000)

        return {
            "success": result.get("success", False),
            "result": result.get("data") if result.get("success") else None,
            "error": result.get("error") if not result.get("success") else None,
            "error_code": result.get("error_code") if not result.get("success") else None,
            "execution_time_ms": execution_time_ms
        }

    except Exception as e:
        execution_time_ms = int((time.time() - start_time) * 1000)
        return {
            "success": False,
            "error": str(e),
            "error_code": "TOOL_ERROR",
            "execution_time_ms": execution_time_ms
        }


async def run_agent_with_google_ai(
    messages: List[Dict[str, str]],
    user_id: str
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Run AI agent using Google AI Studio (Gemini).
    
    Args:
        messages: Conversation history
        user_id: Authenticated user ID
        
    Returns:
        Tuple of (assistant_response, tool_calls_list)
    """
    try:
        # Import Google AI library
        import google.generativeai as genai
        
        # Configure API
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Create model
        model = genai.GenerativeModel(GOOGLE_MODEL)
        
        # Build conversation context
        conversation_text = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" 
            for msg in messages
        ])
        
        # Create prompt with tool instructions
        prompt = f"""You are a helpful task management assistant. You have access to these tools:

1. add_task(title, description) - Create a new task
2. list_tasks() - List all tasks
3. complete_task(task_id) - Mark a task as complete
4. delete_task(task_id) - Delete a task
5. update_task(task_id, title, description, completed) - Update a task

Current conversation:
{conversation_text}

To use a tool, respond with: TOOL: tool_name(arguments)
Example: TOOL: add_task(title="Buy groceries", description="Weekly shopping")

Otherwise, respond naturally to help the user."""

        # Generate response
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        tool_calls_log = []
        
        # Check if response contains tool call
        if response_text.startswith("TOOL:"):
            # Parse tool call
            try:
                tool_part = response_text.replace("TOOL:", "").strip()
                tool_name = tool_part.split("(")[0].strip()
                args_str = tool_part[tool_part.find("(")+1:tool_part.rfind(")")]
                
                # Parse arguments (simplified)
                arguments = {}
                if args_str:
                    for arg in args_str.split(","):
                        if "=" in arg:
                            key, value = arg.split("=", 1)
                            arguments[key.strip()] = value.strip().strip('"\'')
                
                # Execute tool
                result = await execute_mcp_tool(tool_name, arguments, user_id)
                
                tool_calls_log.append({
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "success": result["success"],
                    "result": result.get("result"),
                    "error": result.get("error"),
                    "execution_time_ms": result.get("execution_time_ms")
                })
                
                # Return tool result
                if result["success"]:
                    return f"I've completed that action for you.", tool_calls_log
                else:
                    return f"Failed to execute action: {result.get('error', 'Unknown error')}", tool_calls_log
                    
            except Exception as e:
                return f"I understood you want to use a tool, but I had trouble parsing it. Could you rephrase? Error: {str(e)}", tool_calls_log
        else:
            # Natural response
            return response_text, tool_calls_log
    
    except Exception as e:
        # Fallback to rule-based AI
        return await run_agent_rule_based(messages, user_id)


async def run_agent_rule_based(
    messages: List[Dict[str, str]],
    user_id: str
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Run rule-based AI agent (fallback when no API key or errors).
    
    Args:
        messages: Conversation history
        user_id: Authenticated user ID
        
    Returns:
        Tuple of (assistant_response, tool_calls_list)
    """
    try:
        tool_calls_log = []
        
        # Get last user message
        last_message = messages[-1]['content'].lower() if messages else ''
        
        # Simple intent detection
        if 'add' in last_message and 'task' in last_message:
            # Extract task title (simplified)
            title = last_message.replace('add', '').replace('task', '').replace('to', '').strip()
            if not title:
                title = 'New Task'
            
            # Call add_task tool
            result = await execute_mcp_tool('add_task', {
                'title': title.title(),
                'description': 'Created via AI chat'
            }, user_id)
            
            tool_calls_log.append({
                'tool_name': 'add_task',
                'arguments': {'title': title, 'description': 'Created via AI chat'},
                'success': result['success'],
                'result': result.get('result'),
                'error': result.get('error'),
                'execution_time_ms': result.get('execution_time_ms')
            })
            
            if result['success']:
                return f"I've created the task '{title.title()}' for you.", tool_calls_log
            else:
                return f"Failed to create task: {result.get('error', 'Unknown error')}", tool_calls_log
        
        elif 'list' in last_message and 'task' in last_message:
            # Call list_tasks tool
            result = await execute_mcp_tool('list_tasks', {}, user_id)
            
            tool_calls_log.append({
                'tool_name': 'list_tasks',
                'arguments': {},
                'success': result['success'],
                'result': result.get('result'),
                'error': result.get('error'),
                'execution_time_ms': result.get('execution_time_ms')
            })
            
            if result['success'] and result.get('result', {}).get('tasks'):
                tasks = result['result']['tasks']
                task_list = '\n'.join([f"{i+1}. {t['title']} ({'✓' if t['completed'] else '○'})" for i, t in enumerate(tasks)])
                return f"You have {len(tasks)} task(s):\n\n{task_list}", tool_calls_log
            else:
                return "You don't have any tasks yet.", tool_calls_log
        
        elif 'complete' in last_message or 'mark' in last_message:
            # For simplicity, complete the first incomplete task
            list_result = await execute_mcp_tool('list_tasks', {'completed': False}, user_id)
            if list_result['success'] and list_result.get('result', {}).get('tasks'):
                task_id = list_result['result']['tasks'][0]['id']
                complete_result = await execute_mcp_tool('complete_task', {'task_id': task_id}, user_id)
                
                tool_calls_log.append({
                    'tool_name': 'complete_task',
                    'arguments': {'task_id': task_id},
                    'success': complete_result['success'],
                    'result': complete_result.get('result'),
                    'error': complete_result.get('error'),
                    'execution_time_ms': complete_result.get('execution_time_ms')
                })
                
                if complete_result['success']:
                    return "I've marked the task as completed.", tool_calls_log
            
            return "No tasks to complete or failed to complete task.", tool_calls_log
        
        elif 'delete' in last_message and 'task' in last_message:
            # For simplicity, delete the first task
            list_result = await execute_mcp_tool('list_tasks', {}, user_id)
            if list_result['success'] and list_result.get('result', {}).get('tasks'):
                task_id = list_result['result']['tasks'][0]['id']
                delete_result = await execute_mcp_tool('delete_task', {'task_id': task_id}, user_id)
                
                tool_calls_log.append({
                    'tool_name': 'delete_task',
                    'arguments': {'task_id': task_id},
                    'success': delete_result['success'],
                    'result': delete_result.get('result'),
                    'error': delete_result.get('error'),
                    'execution_time_ms': delete_result.get('execution_time_ms')
                })
                
                if delete_result['success']:
                    return "I've deleted the task.", tool_calls_log
            
            return "No tasks to delete or failed to delete task.", tool_calls_log
        
        else:
            # Default response with helpful suggestions
            return """I can help you manage tasks! Try these commands:

• "Add a task to review docs" - Create a new task
• "List my tasks" - See all your tasks
• "Mark task as complete" - Complete a task
• "Delete the first task" - Remove a task

I'm here to make task management easier!""", tool_calls_log
    
    except Exception as e:
        # Return error message
        return f"Sorry, I encountered an error: {str(e)}. Please try again.", []


async def run_agent_with_tools(
    messages: List[Dict[str, str]],
    user_id: str
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Main entry point - routes to appropriate AI provider.
    
    Args:
        messages: Conversation history
        user_id: Authenticated user ID
        
    Returns:
        Tuple of (assistant_response, tool_calls_list)
    """
    # Check if AI is enabled
    if os.getenv("AI_ENABLED", "true").lower() != "true":
        return await run_agent_rule_based(messages, user_id)
    
    # Route to appropriate provider
    if AI_PROVIDER == "google" and GOOGLE_API_KEY and GOOGLE_API_KEY != "your-google-aistudio-api-key-here":
        try:
            return await run_agent_with_google_ai(messages, user_id)
        except Exception as e:
            # Fallback to rule-based on error
            return await run_agent_rule_based(messages, user_id)
    else:
        # Use rule-based AI (no API key required)
        return await run_agent_rule_based(messages, user_id)
