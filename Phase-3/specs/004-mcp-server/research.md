# Research: MCP Server & Task Tooling Layer

**Feature**: 004-mcp-server
**Date**: 2026-02-18
**Status**: Complete

## MCP SDK Integration

### Decision: Use Official MCP Python SDK
The Model Context Protocol (MCP) Python SDK provides the standard interface for exposing tools to AI agents.

**Installation**:
```bash
pip install mcp
```

**Server Initialization Pattern**:
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

mcp_server = Server("phase-3-task-tools")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp.server.create_initialization_options()
        )
```

**Tool Registration**:
```python
from mcp.server import Server
from pydantic import BaseModel

@mcp_server.tool()
async def add_task(title: str, description: str | None = None) -> dict:
    """Add a new task for the authenticated user."""
    # Implementation
    pass
```

**Alternatives Considered**:
- Custom JSON-RPC implementation: Rejected due to lack of standardization
- LangChain tools: Rejected - not MCP-compliant, ties to specific AI framework

## Tool Schema Design

### Decision: Pydantic-Based Schema Validation
Use Pydantic models for strict input/output validation with JSON Schema generation.

**Input Schema Pattern**:
```python
from pydantic import BaseModel, Field

class AddTaskInput(BaseModel):
    user_id: str = Field(..., description="Authenticated user ID")
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
```

**Output Schema Pattern**:
```python
class ToolSuccessResponse(BaseModel):
    success: bool = True
    data: dict
    tool_name: str
    execution_time_ms: int

class ToolErrorResponse(BaseModel):
    success: bool = False
    error: str
    error_code: str
    tool_name: str
```

**Validation Rules**:
- All required fields enforced at Pydantic model level
- String length limits prevent database bloat
- Type coercion handled automatically by Pydantic
- Custom validators for business rules (e.g., user_id format)

## Database Connection Handling

### Decision: SQLModel Async Sessions with Connection Pooling
Reuse existing Phase-2 database infrastructure with stateless session management.

**Session Pattern**:
```python
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool  # For serverless

# Neon-compatible engine configuration
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,  # Serverless-compatible
    echo=False
)

async def get_session() -> Session:
    """Create a new session per tool invocation (stateless)."""
    with Session(engine) as session:
        yield session
```

**Neon PostgreSQL Considerations**:
- Use `StaticPool` for serverless compatibility (no persistent connections)
- Connection string from environment: `DATABASE_URL`
- SSL mode required: `?sslmode=require`

**Transaction Handling**:
```python
try:
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"success": True, "data": task.model_dump()}
except Exception as e:
    session.rollback()
    return {"success": False, "error": str(e)}
```

## Logging & Traceability Strategy

### Decision: Structured JSON Logging with Security Event Tracking
Reuse existing Phase-3 logging infrastructure from `backend/src/utils/logging.py`.

**Log Structure**:
```python
import json
from datetime import datetime

def log_tool_invocation(user_id: str, tool_name: str, inputs: dict, result: dict):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "tool_invocation",
        "user_id": user_id,
        "tool_name": tool_name,
        "inputs": sanitize_inputs(inputs),
        "success": result.get("success", False),
        "execution_time_ms": result.get("execution_time_ms", 0)
    }
    logger.info(json.dumps(log_entry))
```

**Security Event Types** (from existing `SecurityEventType` enum):
- `TOOL_INVOCATION`: Every tool execution
- `VALIDATION_FAILURE`: Input schema validation errors
- `OWNERSHIP_VIOLATION`: Cross-user access attempts
- `DATABASE_ERROR`: Persistence failures

**Audit Trail Requirements**:
- Log every tool invocation with user_id and timestamp
- Log validation failures with rejected input summary
- Log ownership violations for security monitoring
- Retain logs for hackathon review (development phase only)

## Serverless Compatibility

### Decision: Stateless Design with HTTP Trigger Model
MCP server designed for serverless deployment (e.g., AWS Lambda, Vercel, Cloudflare Workers).

**Key Constraints**:
- No in-memory state between invocations
- Database connection created per request
- No background threads or async tasks
- Cold start optimization: minimal dependencies

**Deployment Pattern**:
```python
# Lambda-style handler
def handler(event, context):
    """Serverless entry point for MCP tool invocation."""
    user_id = event["user_id"]
    tool_name = event["tool_name"]
    inputs = event["inputs"]
    
    # Execute tool
    result = execute_tool(tool_name, user_id, inputs)
    
    # Log invocation
    log_tool_invocation(user_id, tool_name, inputs, result)
    
    return result
```

## Summary of Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| MCP Library | Official MCP SDK | Standard compliance, future-proof |
| Schema Validation | Pydantic | Type safety, auto JSON Schema generation |
| Database Sessions | SQLModel async | Reuse Phase-2 infrastructure |
| Connection Pooling | StaticPool | Serverless compatibility (Neon) |
| Logging | Structured JSON | Audit trail, security event tracking |
| Deployment | Stateless HTTP | Serverless-compatible architecture |

## Unresolved Questions

None - all technical decisions resolved with documented rationales.
