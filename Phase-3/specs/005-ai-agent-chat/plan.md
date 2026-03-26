# Implementation Plan: AI Agent & Stateless Chat Orchestration

**Branch**: `005-ai-agent-chat` | **Date**: 2026-02-18 | **Spec**: [specs/005-ai-agent-chat/spec.md](../spec.md)
**Input**: Feature specification from `/specs/005-ai-agent-chat/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement an AI agent using OpenAI Agents SDK that orchestrates MCP tools for natural language task management. Build a stateless POST /api/{user_id}/chat endpoint that fetches conversation history from database on every request, executes the agent with MCP tools, persists messages, and returns responses with tool call traces. All state persists through database only—zero in-memory conversation state.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: OpenAI Agents SDK, FastAPI, SQLModel, MCP SDK (for tool integration)
**Storage**: Neon Serverless PostgreSQL (existing database from Phase-2/Phase-3)
**Testing**: pytest, pytest-cov, pytest-asyncio, httpx (for API testing)
**Target Platform**: Serverless-compatible Python runtime
**Project Type**: Backend API layer (AI agent orchestration)
**Performance Goals**: Chat responses within 5 seconds p95 latency, conversation history retrieval <500ms
**Constraints**: Fully stateless (no in-memory state), single request-response cycle (no streaming), serverless-compatible
**Scale/Scope**: Multi-user chat with conversation persistence, agent invokes 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)

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
specs/005-ai-agent-chat/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── chat-api.json        # Chat endpoint request/response schema
│   └── agent-config.json    # Agent behavior configuration
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── chat.py              # POST /api/{user_id}/chat endpoint
│   ├── agent/
│   │   ├── __init__.py          # Agent initialization
│   │   ├── config.py            # Agent behavior configuration
│   │   └── tools.py             # MCP tool integration for agent
│   ├── models/
│   │   ├── conversation.py      # Conversation and Message models
│   │   └── task.py              # Reuse existing Task model
│   └── services/
│       ├── conversation_service.py  # Conversation persistence logic
│       └── agent_service.py         # Agent orchestration service
└── tests/
    ├── agent/
    │   ├── test_agent_tools.py    # Agent tool invocation tests
    │   └── test_config.py         # Agent configuration tests
    └── integration/
        └── test_chat_flow.py      # End-to-end chat flow tests
```

**Structure Decision**: Using existing `backend/` structure from Phase-3. Agent orchestration is a new module under `backend/src/agent/` that integrates with existing MCP server and database layer. Chat endpoint added to `backend/src/api/`. New models in `backend/src/models/`.

## Complexity Tracking

All constitution compliance items pass - no complexity justification needed.

## Phase 0: Research Plan

### Research Tasks

1. **OpenAI Agents SDK Integration**
   - Research official OpenAI Agents SDK initialization and configuration
   - Document tool registration patterns for MCP tools
   - Identify agent behavior rule configuration approach

2. **Conversation History Management**
   - Research efficient conversation history retrieval patterns
   - Document context window management for LLM
   - Identify message formatting for agent consumption

3. **Stateless Agent Orchestration**
   - Research stateless agent execution patterns
   - Document tool call capture and result handling
   - Identify error handling patterns for tool failures

4. **Database Schema Design**
   - Research Conversation and Message model design patterns
   - Document user scoping and indexing strategies
   - Identify migration approach for new tables

## Phase 1: Design Deliverables

### data-model.md
- Conversation model: id, user_id, created_at, updated_at
- Message model: id, conversation_id, role (user/assistant), content, tool_calls, created_at
- Relationships: Conversation has-many Messages, all scoped by user_id
- Indexes: user_id, conversation_id, created_at for efficient history retrieval

### contracts/
- `chat-api.json`: Chat endpoint request/response OpenAPI schema
- `agent-config.json`: Agent behavior configuration (instructions, tool rules, error handling)

### quickstart.md
- Chat endpoint setup instructions
- Agent configuration guide
- Conversation history management
- Testing instructions with example requests

### research.md
- OpenAI Agents SDK integration findings
- Conversation history management patterns
- Stateless orchestration approach
- Database schema design decisions

## Next Steps

After this plan is complete, the next phase is `/sp.tasks` to break this implementation into actionable tasks.
