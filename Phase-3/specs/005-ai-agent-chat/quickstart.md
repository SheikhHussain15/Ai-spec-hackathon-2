# Quickstart: AI Agent & Stateless Chat Orchestration

**Feature**: 005-ai-agent-chat
**Version**: 1.0.0
**Last Updated**: 2026-02-18

## Overview

The AI Agent & Stateless Chat Orchestration feature enables users to manage tasks through natural language conversation with an AI agent. The agent invokes MCP tools to perform task operations and maintains conversation history in the database.

## Prerequisites

- Python 3.11+
- OpenAI API key
- Existing Phase-3 backend with MCP server
- Neon PostgreSQL database

## Installation

### 1. Install Dependencies

```bash
cd backend
pip install openai-agents
```

### 2. Configure Environment

Create or update `.env`:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Database
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require

# Security
BETTER_AUTH_SECRET=your-secret-key-here
```

### 3. Run Database Migration

```bash
# Apply conversation models migration
psql $DATABASE_URL -f migrations/005_add_conversation_models.sql
```

## Running the Chat Endpoint

### Start the Backend

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

The chat endpoint will be available at:
- `POST /api/{user_id}/chat`

## API Usage Examples

### Example 1: Start New Conversation

**Request**:
```bash
curl -X POST http://localhost:8000/api/user-123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Add a task to review the project documentation tomorrow"
  }'
```

**Response**:
```json
{
  "success": true,
  "response": "I've created a task for you to review the project documentation tomorrow.",
  "conversation_id": "conv-abc123",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "arguments": {
        "title": "Review the project documentation tomorrow",
        "description": null
      },
      "success": true,
      "result": {
        "id": "task-xyz789",
        "title": "Review the project documentation tomorrow",
        "completed": false
      },
      "execution_time_ms": 45
    }
  ]
}
```

### Example 2: Continue Existing Conversation

**Request**:
```bash
curl -X POST http://localhost:8000/api/user-123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "What tasks do I have?",
    "conversation_id": "conv-abc123"
  }'
```

**Response**:
```json
{
  "success": true,
  "response": "You have 1 task:\n\n1. [ ] Review the project documentation tomorrow",
  "conversation_id": "conv-abc123",
  "tool_calls": [
    {
      "tool_name": "list_tasks",
      "arguments": {
        "user_id": "user-123"
      },
      "success": true,
      "result": {
        "tasks": [
          {
            "id": "task-xyz789",
            "title": "Review the project documentation tomorrow",
            "completed": false
          }
        ],
        "count": 1
      },
      "execution_time_ms": 32
    }
  ]
}
```

### Example 3: Complete a Task

**Request**:
```bash
curl -X POST http://localhost:8000/api/user-123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Mark the first task as done"
  }'
```

**Response**:
```json
{
  "success": true,
  "response": "I've marked the task 'Review the project documentation tomorrow' as completed.",
  "conversation_id": "conv-def456",
  "tool_calls": [
    {
      "tool_name": "complete_task",
      "arguments": {
        "user_id": "user-123",
        "task_id": "task-xyz789"
      },
      "success": true,
      "result": {
        "id": "task-xyz789",
        "title": "Review the project documentation tomorrow",
        "completed": true
      },
      "execution_time_ms": 38
    }
  ]
}
```

### Example 4: Error Handling - Task Not Found

**Request**:
```bash
curl -X POST http://localhost:8000/api/user-123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Delete task abc123"
  }'
```

**Response**:
```json
{
  "success": true,
  "response": "I couldn't find that task. It might have been deleted already or the reference might be outdated. Would you like me to list your current tasks?",
  "conversation_id": "conv-ghi789",
  "tool_calls": [
    {
      "tool_name": "delete_task",
      "arguments": {
        "user_id": "user-123",
        "task_id": "abc123"
      },
      "success": false,
      "error": "Task not found",
      "error_code": "NOT_FOUND",
      "execution_time_ms": 15
    }
  ]
}
```

## Get Conversations

**Request**:
```bash
curl -X GET http://localhost:8000/api/user-123/conversations \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response**:
```json
{
  "success": true,
  "conversations": [
    {
      "id": "conv-abc123",
      "title": "Add a task to review",
      "created_at": "2026-02-18T12:00:00Z",
      "updated_at": "2026-02-18T12:05:00Z",
      "message_count": 4
    }
  ]
}
```

## Get Conversation History

**Request**:
```bash
curl -X GET http://localhost:8000/api/user-123/conversations/conv-abc123 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response**:
```json
{
  "success": true,
  "conversation": {
    "id": "conv-abc123",
    "title": "Add a task to review",
    "created_at": "2026-02-18T12:00:00Z",
    "updated_at": "2026-02-18T12:05:00Z"
  },
  "messages": [
    {
      "id": "msg-001",
      "role": "user",
      "content": "Add a task to review the project documentation tomorrow",
      "tool_calls": null,
      "created_at": "2026-02-18T12:00:00Z"
    },
    {
      "id": "msg-002",
      "role": "assistant",
      "content": "I've created a task for you...",
      "tool_calls": {
        "calls": [
          {
            "tool_name": "add_task",
            "arguments": {...},
            "result": {...}
          }
        ]
      },
      "created_at": "2026-02-18T12:00:01Z"
    }
  ]
}
```

## Testing

### Run Unit Tests

```bash
cd backend
pytest tests/agent/ -v
```

### Run Integration Tests

```bash
cd backend
pytest tests/integration/test_chat_flow.py -v
```

## Troubleshooting

### Agent Not Responding

**Error**: Timeout or no response

**Solution**:
1. Verify `OPENAI_API_KEY` is set correctly
2. Check OpenAI API status
3. Verify network connectivity

### Tool Invocations Failing

**Error**: `TOOL_ERROR` in response

**Solution**:
1. Verify MCP server is running
2. Check database connection
3. Review tool execution logs

### Conversation History Not Persisting

**Error**: Messages not saved

**Solution**:
1. Verify database migration applied
2. Check `DATABASE_URL` configuration
3. Review database permissions

## Architecture Notes

- **Stateless Design**: No in-memory conversation state
- **Full History Fetch**: Every request retrieves conversation history from database
- **Tool Transparency**: All tool invocations logged and returned in response
- **User Isolation**: All queries scoped by user_id
- **Error Handling**: Graceful errors with user-friendly messages

## Next Steps

- Integrate with frontend chat UI
- Add conversation search functionality
- Implement conversation archiving
- Add multi-turn conversation optimization
