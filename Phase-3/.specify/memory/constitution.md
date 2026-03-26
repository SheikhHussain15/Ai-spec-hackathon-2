<!--
Sync Impact Report:
- Version change: 1.1.0 → 2.0.0
- Modified principles: All principles redefined for AI-Powered Todo Chatbot architecture
- Added sections: AI Architecture Standards, Backend Standards, Database Standards, Security Standards, Operational Constraints, Deliverables, Success Criteria
- Removed sections: None (previous principles generalized, now specialized for MCP + Agents SDK)
- Templates requiring updates: ✅ plan-template.md (Constitution Check updated with AI-specific compliance items)
- Follow-up TODOs: None
-->
# Phase-3 AI-Powered Todo Chatbot Constitution

**Project**: Phase-3 — AI-Powered Todo Chatbot (MCP + Agents SDK Architecture)

## Core Principles

### Deterministic Tool Execution
AI must plan actions explicitly; Tools execute plans without deviation; All tool invocations must be logged and traceable; No autonomous behavior outside defined tool schemas.

### Stateless Server Architecture
Server must hold zero runtime conversation state; All state must persist through database only; Every request must fetch conversation history from database; Server restart must not affect conversation continuity.

### Clear Separation of Concerns
UI layer must be isolated from Agent logic; Agent layer must be isolated from MCP tools; MCP tools must be isolated from database directly; Backend orchestration only—no direct frontend-to-MCP calls.

### Security and User Isolation
All chat endpoints require valid JWT authentication; Agent must operate only within authenticated user context; MCP tools must validate user_id before executing; No cross-user data exposure under any condition; User isolation inherited from Phase-1 & Phase-2.

### Spec-Driven Agentic Development
All development must follow spec → plan → tasks → implementation workflow; No manual coding allowed; All code generated via Qwen Code using specialized agents; Every feature must be traceable back to specification.

## AI Architecture Standards

### OpenAI Agents SDK Usage
AI logic must use OpenAI Agents SDK exclusively; Agent behavior must be rule-defined and predictable; No custom AI orchestration outside Agents SDK.

### MCP Tool Enforcement
All task operations must be executed via MCP tools; No direct database access from agent; MCP tools must be stateless; MCP tools must persist state only through database.

### Tool Schema Validation
Tool schemas must be strictly validated before execution; No dynamic or unvalidated tool invocation; All tool inputs must conform to defined schemas.

## Backend Standards

### Chat Endpoint Specification
Chat endpoint must be: POST /api/{user_id}/chat; Endpoint must require JWT authentication; Endpoint must validate user_id matches JWT claims.

### Conversation State Management
Server must fetch conversation history from database on every request; Server must store user and assistant messages persistently; Server must hold zero runtime conversation state.

### User Isolation Enforcement
All operations must respect authenticated user isolation; No cross-user queries or data access; Backend must validate JWT before any operation.

## Database Standards

### Task Model Reuse
Task model must be reused from Phase-2; Task model must maintain compatibility with existing schema.

### Conversation and Message Models
New models required: Conversation and Message; All records must be scoped by user_id; Conversation must resume correctly after server restart.

### User Scoping
All database records must be scoped by user_id; No global or unscoped queries allowed; Database queries must enforce user isolation at query level.

## Security Standards

### JWT Authentication
All chat endpoints require valid JWT; JWT must be verified using shared secret (BETTER_AUTH_SECRET); User identity must be derived from JWT claims only; Invalid, missing, or expired tokens must return 401 Unauthorized.

### Agent Context Enforcement
Agent must only operate within authenticated user context; No agent operations outside user scope; Agent must validate user context before tool invocation.

### MCP Tool Validation
MCP tools must validate user_id before executing; No tool execution without valid user context; Tools must reject cross-user operation attempts.

### Data Exposure Prevention
No cross-user data exposure under any condition; Database queries must filter by user_id; API responses must never include other users' data.

## Operational Constraints

### Serverless Compatibility
Architecture must be compatible with serverless deployment; No background workers allowed; No persistent connections or websockets.

### Stateless Operations
No hidden state between requests; All state must persist in database; Server restart must not affect functionality.

### Backend Orchestration Only
No direct frontend-to-MCP calls; All MCP tool calls must go through backend; Backend must orchestrate all agent and tool interactions.

## Deliverables

### Required Components
MCP server exposing required task tools; FastAPI chat endpoint integrating Agents SDK; Persistent conversation storage in Neon PostgreSQL; ChatKit frontend integration.

### Repository Structure
GitHub repository with /frontend, /backend, /specs directories; Database migration scripts included; Setup documentation in README.

### Documentation
README must include setup instructions; Architecture documentation must explain MCP + Agents SDK integration; API documentation must document all endpoints.

## Success Criteria

### Functional Success
Users can manage tasks entirely through natural language; Agent correctly selects and invokes MCP tools; Conversation context persists across requests and restarts.

### Architectural Success
Server remains fully stateless; Tool invocations are logged and traceable; All operations are deterministic and predictable.

### Reviewability
Hackathon reviewers can trace implementation back to specs; All code is generated via Qwen Code; No manual coding deviations exist.

## Governance

All development must comply with these principles; Changes to the constitution require explicit documentation; Each implementation phase must be traceable to specification; Code reviews must verify compliance with all architectural and security standards.

**Version**: 2.0.0 | **Ratified**: 2026-02-09 | **Last Amended**: 2026-02-18
