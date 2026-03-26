# Quickstart: MCP Server & Task Tooling Layer

**Feature**: 004-mcp-server
**Version**: 1.0.0
**Last Updated**: 2026-02-18

## Overview

The MCP Server exposes 5 stateless task management tools via the Model Context Protocol (MCP). Tools are invoked by AI agents and execute against a Neon PostgreSQL database.

**Tools**:
- `add_task` - Create a new task
- `list_tasks` - List all tasks for a user
- `complete_task` - Mark a task as completed
- `delete_task` - Delete a task
- `update_task` - Update task fields

## Prerequisites

- Python 3.11+
- Neon PostgreSQL database (connection string in `.env`)
- Existing Phase-2 backend with Task model

## Installation

### 1. Install Dependencies

```bash
cd backend
pip install mcp pydantic sqlmodel psycopg2-binary
```

### 2. Configure Environment

Create or update `.env`:

```bash
# Database
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require

# Security
BETTER_AUTH_SECRET=your-secret-key-here

# MCP Server
MCP_SERVER_NAME=phase-3-task-tools
LOG_LEVEL=INFO
```

## Running the MCP Server

### Development Mode (stdio transport)

```bash
cd backend
python -m src.mcp.server
```

### Production Mode (HTTP transport for serverless)

```bash
# Via FastAPI integration (recommended)
uvicorn src.mcp.http_adapter:app --host 0.0.0.0 --port 8000
```

## Tool Invocation Examples

### Example 1: Add Task

**Input**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete MCP integration",
  "description": "Finish implementing all 5 MCP tools"
}
```

**Expected Output**:
```json
{
  "success": true,
  "data": {
    "id": "task-uuid-here",
    "title": "Complete MCP integration",
    "description": "Finish implementing all 5 MCP tools",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "completed": false,
    "created_at": "2026-02-18T12:00:00Z",
    "updated_at": "2026-02-18T12:00:00Z"
  },
  "tool_name": "add_task",
  "execution_time_ms": 45
}
```

### Example 2: List Tasks

**Input**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Expected Output**:
```json
{
  "success": true,
  "data": [
    {
      "id": "task-uuid-1",
      "title": "Complete MCP integration",
      "description": "Finish implementing all 5 MCP tools",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "completed": false,
      "created_at": "2026-02-18T12:00:00Z",
      "updated_at": "2026-02-18T12:00:00Z"
    }
  ],
  "tool_name": "list_tasks",
  "execution_time_ms": 32
}
```

### Example 3: Complete Task

**Input**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "task-uuid-here"
}
```

**Expected Output**:
```json
{
  "success": true,
  "data": {
    "id": "task-uuid-here",
    "title": "Complete MCP integration",
    "completed": true,
    "updated_at": "2026-02-18T12:05:00Z"
  },
  "tool_name": "complete_task",
  "execution_time_ms": 38
}
```

### Example 4: Update Task

**Input**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "task-uuid-here",
  "title": "Updated task title",
  "completed": true
}
```

**Expected Output**:
```json
{
  "success": true,
  "data": {
    "id": "task-uuid-here",
    "title": "Updated task title",
    "description": "Finish implementing all 5 MCP tools",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "completed": true,
    "created_at": "2026-02-18T12:00:00Z",
    "updated_at": "2026-02-18T12:10:00Z"
  },
  "tool_name": "update_task",
  "execution_time_ms": 42
}
```

### Example 5: Delete Task

**Input**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "task-uuid-here"
}
```

**Expected Output**:
```json
{
  "success": true,
  "data": {
    "deleted": true,
    "task_id": "task-uuid-here"
  },
  "tool_name": "delete_task",
  "execution_time_ms": 35
}
```

## Error Handling Examples

### Validation Error (422)

```json
{
  "success": false,
  "error": "Input validation failed: title - string too short",
  "error_code": "VALIDATION_ERROR",
  "tool_name": "add_task",
  "details": {
    "field": "title",
    "reason": "minLength is 1",
    "received": ""
  }
}
```

### Ownership Violation (403)

```json
{
  "success": false,
  "error": "Access denied: You do not own this resource",
  "error_code": "OWNERSHIP_VIOLATION",
  "tool_name": "update_task",
  "details": {
    "requested_resource_id": "task-uuid-123",
    "authenticated_user_id": "user-uuid-456"
  }
}
```

### Not Found (404)

```json
{
  "success": false,
  "error": "Resource not found: Task with ID nonexistent-uuid",
  "error_code": "NOT_FOUND",
  "tool_name": "delete_task",
  "details": {
    "resource_type": "Task",
    "resource_id": "nonexistent-uuid"
  }
}
```

## Testing

### Run Unit Tests

```bash
cd backend
pytest tests/mcp/test_tools.py -v
```

### Run Integration Tests

```bash
cd backend
pytest tests/integration/test_mcp_flow.py -v
```

### Manual Testing with MCP Inspector

```bash
# Install MCP inspector
npx @modelcontextprotocol/inspector

# Run your MCP server
python -m src.mcp.server

# In another terminal, connect inspector
# Follow inspector prompts to test tools
```

## Troubleshooting

### Database Connection Failed

**Error**: `DATABASE_ERROR: connection timeout`

**Solution**:
1. Verify `DATABASE_URL` in `.env`
2. Ensure Neon database is accessible
3. Check SSL mode: `?sslmode=require`

### Ownership Violation

**Error**: `OWNERSHIP_VIOLATION: Access denied`

**Solution**:
- Ensure `user_id` in request matches task owner
- This is expected behavior for cross-user access attempts

### Validation Errors

**Error**: `VALIDATION_ERROR: Input validation failed`

**Solution**:
- Check input against tool schema in `contracts/tool-schemas.json`
- Verify UUID format for `user_id` and `task_id`
- Ensure `title` is 1-200 characters

## Architecture Notes

- **Stateless**: No in-memory state between invocations
- **User Isolation**: All queries scoped by `user_id`
- **Logging**: All invocations logged for traceability
- **Serverless**: Compatible with AWS Lambda, Vercel, etc.

## Next Steps

- Integrate MCP server with OpenAI Agents SDK
- Implement chat endpoint in FastAPI
- Add ChatKit frontend integration
