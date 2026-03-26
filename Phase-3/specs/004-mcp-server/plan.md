# Implementation Plan: MCP Server & Task Tooling Layer

**Branch**: `001-mcp-server` | **Date**: 2026-02-18 | **Spec**: [specs/004-mcp-server/spec.md](../spec.md)
**Input**: Feature specification from `/specs/004-mcp-server/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a stateless MCP server using the Official MCP SDK that exposes 5 task management tools (add_task, list_tasks, complete_task, delete_task, update_task). Each tool validates input schemas strictly, enforces user_id ownership before database operations, and persists changes to Neon PostgreSQL. The MCP layer contains no AI logic, no direct frontend communication, and no cross-user data access.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: MCP SDK (official), SQLModel, FastAPI (for integration), psycopg2-binary (Neon driver)
**Storage**: Neon Serverless PostgreSQL (existing database from Phase-2)
**Testing**: pytest, pytest-cov, pytest-asyncio
**Target Platform**: Serverless-compatible Python runtime
**Project Type**: Backend API layer (MCP server)
**Performance Goals**: Tool invocations complete within 500ms p95 latency
**Constraints**: Fully stateless (no in-memory state), serverless-compatible, no background workers
**Scale/Scope**: Single-user task management via AI agent invocation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Deterministic Tool Execution Compliance
- [x] AI will plan actions explicitly before tool execution
- [x] All tool invocations will be logged and traceable
- [x] No autonomous behavior outside defined tool schemas

### Stateless Server Architecture Compliance
- [x] Server will hold zero runtime conversation state
- [x] All state will persist through database only
- [x] Every request will fetch conversation history from database
- [x] Server restart will not affect conversation continuity

### Clear Separation of Concerns Compliance
- [x] UI layer will be isolated from Agent logic
- [x] Agent layer will be isolated from MCP tools
- [x] Backend orchestration only—no direct frontend-to-MCP calls

### Security and User Isolation Compliance
- [x] All chat endpoints will require valid JWT authentication
- [x] Agent will operate only within authenticated user context
- [x] MCP tools will validate user_id before executing
- [x] No cross-user data exposure under any condition

### Spec-Driven Agentic Development Compliance
- [x] Development will follow spec → plan → tasks → implementation workflow
- [x] No manual coding will be performed
- [x] All code will be generated via Qwen Code using specialized agents

### AI Architecture Standards Compliance
- [x] AI logic will use OpenAI Agents SDK exclusively
- [x] All task operations will be executed via MCP tools
- [x] No direct database access from agent
- [x] MCP tools will be stateless and persist state only through database
- [x] Tool schemas will be strictly validated before execution

### Backend Standards Compliance
- [x] Chat endpoint will be: POST /api/{user_id}/chat
- [x] Server will fetch conversation history from database on every request
- [x] Server will store user and assistant messages persistently
- [x] All operations will respect authenticated user isolation

### Database Standards Compliance
- [x] Task model will be reused from Phase-2
- [x] New models: Conversation and Message will be created
- [x] All records will be scoped by user_id
- [x] Conversation will resume correctly after server restart

### Security Standards Compliance
- [x] All chat endpoints will require valid JWT
- [x] JWT will be verified using shared secret (BETTER_AUTH_SECRET)
- [x] User identity will be derived from JWT claims only
- [x] Invalid, missing, or expired tokens will return 401 Unauthorized
- [x] No hardcoded secrets or credentials in source code

### Operational Constraints Compliance
- [x] Architecture will be compatible with serverless deployment
- [x] No background workers will be used
- [x] No hidden state between requests
- [x] No direct frontend-to-MCP calls (backend orchestration only)

**GATE RESULT**: All compliance items checked - proceeding to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/004-mcp-server/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── tool-schemas.json    # MCP tool input/output schemas
│   └── error-codes.json     # Standardized error taxonomy
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── mcp/
│   │   ├── __init__.py          # MCP server initialization
│   │   ├── server.py            # MCP server instance
│   │   ├── tools/
│   │   │   ├── __init__.py      # Tool registry
│   │   │   ├── add_task.py      # add_task tool handler
│   │   │   ├── list_tasks.py    # list_tasks tool handler
│   │   │   ├── complete_task.py # complete_task tool handler
│   │   │   ├── delete_task.py   # delete_task tool handler
│   │   │   └── update_task.py   # update_task tool handler
│   │   └── schemas/
│   │       ├── __init__.py      # Shared schema definitions
│   │       ├── inputs.py        # Tool input validation schemas
│   │       └── outputs.py       # Tool output response schemas
│   ├── models/
│   │   └── task.py              # Reuse existing Task model from Phase-2
│   └── utils/
│       └── logging.py           # Reuse existing logging infrastructure
└── tests/
    ├── mcp/
    │   ├── test_tools.py        # MCP tool unit tests
    │   └── test_schemas.py      # Schema validation tests
    └── integration/
        └── test_mcp_flow.py     # End-to-end MCP tool flow tests
```

**Structure Decision**: Using existing `backend/` structure from Phase-2/Phase-3. MCP server is a new module under `backend/src/mcp/` that integrates with existing models and database layer. No new project structure needed.

## Complexity Tracking

All constitution compliance items pass - no complexity justification needed.

## Phase 0: Research Plan

### Research Tasks

1. **MCP SDK Integration**
   - Research official MCP SDK installation and initialization patterns
   - Document tool registration and schema definition approach
   - Identify serverless compatibility requirements

2. **Tool Schema Design**
   - Research JSON Schema best practices for MCP tools
   - Document input validation patterns with Pydantic
   - Define error response standardization approach

3. **Database Integration**
   - Research SQLModel async session handling in stateless context
   - Document Neon PostgreSQL connection pooling for serverless
   - Identify transaction handling for tool operations

4. **Logging & Traceability**
   - Research structured logging patterns for tool invocations
   - Document audit trail requirements for hackathon reviewability
   - Identify log correlation patterns (request ID, user_id, tool_name)

## Phase 1: Design Deliverables

### data-model.md
- Document existing Task model reuse (fields, validation rules)
- Define any new models if needed (tool execution logs)
- Document user_id scoping enforcement at query level

### contracts/
- `tool-schemas.json`: Complete MCP tool schemas (inputs/outputs)
- `error-codes.json`: Standardized error taxonomy with HTTP status codes

### quickstart.md
- MCP server setup instructions
- Local development configuration
- Tool invocation examples
- Testing instructions

### research.md
- MCP SDK integration findings
- Tool schema design decisions
- Database connection handling patterns
- Logging strategy

## Next Steps

After this plan is complete, the next phase is `/sp.tasks` to break this implementation into actionable tasks.
