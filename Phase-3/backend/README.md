# Backend for Multi-User Todo Web Application

This is the backend service for the multi-user todo web application with JWT-based authentication.

## Features

- JWT-based authentication using Better Auth
- User data isolation
- RESTful API endpoints for task management
- **AI Agent Chat** - Natural language task management via OpenAI Agents SDK
- FastAPI framework with automatic API documentation
- SQLModel for database operations with Neon Serverless PostgreSQL
- Serverless-compatible database session management

## Prerequisites

- Python 3.11+
- pip

## Setup

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies:

```bash
pip install poetry
poetry install
```

Or if you prefer pip:

```bash
pip install -r requirements.txt
```

4. Set up environment variables (see `.env.example`)

## Environment Variables

Create a `.env` file in the backend root directory with the following variables:

```bash
BETTER_AUTH_SECRET=your_jwt_secret_key_here
DATABASE_URL=your_neon_postgres_connection_string
```

## Running the Application

```bash
# Using poetry
poetry run uvicorn src.main:app --reload --port 8000

# Using pip
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` and the interactive documentation at `http://localhost:8000/docs`.

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### User Endpoints
- `GET /api/users/{user_id}` - Get user information

### Task Management Endpoints
- `GET /api/tasks/{user_id}/tasks` - Get all tasks for a user
- `POST /api/tasks/{user_id}/tasks` - Create a new task for a user
- `GET /api/tasks/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{user_id}/tasks/{task_id}` - Update a specific task
- `PATCH /api/tasks/{user_id}/tasks/{task_id}/complete` - Update only the completion status
- `DELETE /api/tasks/{user_id}/tasks/{task_id}` - Delete a specific task

For detailed API documentation, see the [Task API Documentation](../docs/task-api-documentation.md).

## Testing

Run the tests using pytest:

```bash
# Using poetry
poetry run pytest

# Using pip
pytest
```

## MCP Server (AI Agent Integration)

This backend includes an MCP (Model Context Protocol) server for AI agent integration. The MCP server exposes stateless task management tools that can be invoked by AI agents.

### MCP Tools

- `add_task` - Create a new task
- `list_tasks` - List all tasks for a user
- `complete_task` - Mark a task as completed
- `delete_task` - Delete a task
- `update_task` - Update task fields

### Running the MCP Server

```bash
# Using stdio transport (for local development)
python -m src.mcp_server.server

# Using HTTP transport (for serverless deployment)
uvicorn src.mcp_server.http_adapter:app --reload --port 8001
```

### MCP HTTP Endpoints

When running with HTTP transport:

- `POST /mcp/invoke` - Invoke an MCP tool
- `GET /mcp/tools` - List available tools

Example tool invocation:

```bash
curl -X POST http://localhost:8001/mcp/invoke \
  -H "Content-Type: application/json" \
  -H "X-User-Id: your-user-id" \
  -d '{
    "tool_name": "add_task",
    "arguments": {
      "title": "My Task",
      "description": "Task description"
    }
  }'
```

### MCP Testing

```bash
# Run MCP schema tests
pytest tests/mcp/test_tool_schemas.py -v

# Run MCP integration tests
pytest tests/mcp/test_integration.py -v

# Run all MCP tests
pytest tests/mcp/ -v
```

### Database Migration for MCP Audit Logs

To enable optional MCP tool execution audit logging:

```bash
# Run the migration script
psql $DATABASE_URL -f migrations/004_add_mcp_tool_logs.sql
```

This creates the `tool_execution_logs` table for tracking all MCP tool invocations.

---

## AI Agent Chat (NEW!)

The backend now includes an AI-powered chat endpoint for natural language task management. Users can interact with an AI agent that invokes MCP tools to manage tasks.

### Setup

1. **Install OpenAI SDK** (already in pyproject.toml):
   ```bash
   pip install openai>=1.0.0
   ```

2. **Set environment variables**:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4-turbo-preview
   ```

3. **Run database migration**:
   ```bash
   psql $DATABASE_URL -f migrations/005_add_conversation_models.sql
   ```

### Chat Endpoints

- `POST /api/{user_id}/chat` - Send a message to the AI agent
- `GET /api/{user_id}/conversations` - List user's conversations
- `GET /api/{user_id}/conversations/{conversation_id}` - Get conversation history

### Example Usage

```bash
# Chat with AI agent
curl -X POST http://localhost:8000/api/user-123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Add a task to review the project docs tomorrow"
  }'
```

### Agent Capabilities

The AI agent can:
- Create tasks via natural language
- List user's tasks
- Complete tasks
- Delete tasks
- Update task details
- Maintain conversation context across messages

For detailed documentation, see `specs/005-ai-agent-chat/quickstart.md`.