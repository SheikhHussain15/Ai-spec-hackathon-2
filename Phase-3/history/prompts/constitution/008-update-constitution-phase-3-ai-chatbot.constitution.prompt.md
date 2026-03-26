---
id: 008
title: update-constitution-phase-3-ai-chatbot
stage: constitution
date: 2026-02-18
surface: agent
model: qwen-code
feature: phase-3-ai-chatbot
branch: 001-auth-security-foundation
user: hr773
command: /sp.constitution
labels: ["constitution", "architecture", "ai-agents", "mcp"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

/sp.constitution 
Project: Phase-3 — AI-Powered Todo Chatbot (MCP + Agents SDK Architecture)

Core principles:
- Deterministic tool execution (AI plans, tools execute)
- Stateless server architecture (no in-memory session state)
- Clear separation of concerns (UI, Agent, MCP tools, DB)
- Security and user isolation inherited from Phase-1 & Phase-2
- Spec-driven, agentic development (no manual coding)

AI architecture standards:
- AI logic must use OpenAI Agents SDK
- All task operations must be executed via MCP tools (no direct DB access from agent)
- MCP tools must be stateless and persist state only through database
- Agent behavior must be rule-defined and predictable
- Tool schemas must be strictly validated

Backend standards:
- Chat endpoint: POST /api/{user_id}/chat
- Server must fetch conversation history from database on every request
- Server must store user and assistant messages persistently
- Server must hold zero runtime conversation state
- All operations must respect authenticated user isolation

Database standards:
- Task model reused from Phase-2
- New models: Conversation and Message
- All records scoped by user_id
- Conversation must resume correctly after server restart

Security standards:
- All chat endpoints require valid JWT
- Agent must only operate within authenticated user context
- MCP tools must validate user_id before executing
- No cross-user data exposure under any condition

Operational constraints:
- Compatible with serverless deployment
- No background workers
- No hidden state between requests
- No direct frontend-to-MCP calls (backend orchestration only)

Deliverables:
- MCP server exposing required task tools
- FastAPI chat endpoint integrating Agents SDK
- Persistent conversation storage
- ChatKit frontend integration
- GitHub repository with /frontend, /backend, /specs
- Database migration scripts
- Setup documentation (README)

Success criteria:
- Users can manage tasks entirely through natural language
- Agent correctly selects and invokes MCP tools
- Conversation context persists across requests and restarts
- Server remains fully stateless
- Tool invocations are logged and traceable
- Hackathon reviewers can trace implementation back to specs

## Response snapshot

Updated constitution from version 1.1.0 to 2.0.0 with comprehensive principles for AI-Powered Todo Chatbot architecture. All user-provided principles were incorporated into five main sections: Core Principles, AI Architecture Standards, Backend Standards, Database Standards, Security Standards, Operational Constraints, Deliverables, Success Criteria, and Governance.

## Outcome

- ✅ Impact: Constitution now specialized for MCP + Agents SDK architecture with deterministic AI execution, stateless server design, and strict security enforcement
- 🧪 Tests: N/A (constitution document update)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: Run /sp.specify to create feature specification for Phase-3 AI Chatbot
- 🧠 Reflection: Constitution upgrade from generic multi-user todo app to specialized AI chatbot architecture required major version bump (2.0.0) due to fundamental architectural redefinition

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): /sp.constitution with full project requirements
- Next experiment: Create feature specification using /sp.specify for Phase-3 AI Chatbot
