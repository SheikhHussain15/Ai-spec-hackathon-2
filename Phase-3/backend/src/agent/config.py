"""
Agent Configuration for AI chat orchestration.

This module defines agent behavior, tool configuration, and conversation settings.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import os


class AgentConfig(BaseModel):
    """Configuration for AI agent behavior."""
    
    model: str = Field(default="gpt-4-turbo-preview")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=100)
    instructions: str = Field(
        default="""You are a helpful task management assistant integrated with a todo application. 
Your primary role is to help users manage their tasks through natural language conversation. 
You have access to task management tools that you can invoke on behalf of the user.

## Behavior Rules:

1. **Task Management**: When the user wants to create, list, complete, delete, or update tasks, use the appropriate tool.

2. **Clarity**: If the user's request is ambiguous (e.g., 'add a task' without details), ask for clarification before invoking tools.

3. **Confirmation**: For destructive operations (delete), confirm with the user if the intent is unclear.

4. **Context**: Maintain conversation context. If the user refers to 'the first task' or 'that task', use the conversation history to identify which task they mean.

5. **Error Handling**: If a tool invocation fails, explain the error to the user in a friendly way and suggest alternatives.

6. **Transparency**: When you invoke tools, briefly explain what you're doing (e.g., 'I'll create that task for you now').

7. **User Isolation**: Only operate on tasks belonging to the authenticated user. Never attempt to access another user's data.

## Available Tools:

- add_task: Create a new task (requires title, optional description)
- list_tasks: List all tasks for the user (optional filter by completion status)
- complete_task: Mark a task as completed (requires task_id)
- delete_task: Delete a task (requires task_id)
- update_task: Update task fields (requires task_id, at least one field to update)
"""
    )


class ToolConfig(BaseModel):
    """Configuration for tool execution."""
    
    timeout_ms: int = Field(default=30000)
    max_retries: int = Field(default=2)
    
    class Config:
        arbitrary_types_allowed = True


class ConversationConfig(BaseModel):
    """Configuration for conversation management."""
    
    auto_create: bool = Field(default=True)
    max_history_messages: int = Field(default=50)
    oldest_to_keep: int = Field(default=5)
    newest_to_keep: int = Field(default=45)
    title_max_length: int = Field(default=200)


class ResponseConfig(BaseModel):
    """Configuration for API responses."""
    
    include_tool_calls: bool = Field(default=True)
    include_conversation_id: bool = Field(default=True)
    streaming: bool = Field(default=False)


# Global configuration instances
agent_config = AgentConfig()
tool_config = ToolConfig()
conversation_config = ConversationConfig()
response_config = ResponseConfig()


def get_openai_api_key() -> str:
    """Get OpenAI API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return api_key


def get_openai_model() -> str:
    """Get OpenAI model from environment or config."""
    return os.getenv("OPENAI_MODEL", agent_config.model)
