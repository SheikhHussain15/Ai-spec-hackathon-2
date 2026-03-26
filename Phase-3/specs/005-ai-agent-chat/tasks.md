# Tasks: AI Agent & Stateless Chat Orchestration

**Input**: Design documents from `/specs/005-ai-agent-chat/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/

**Tests**: Optional - minimal test coverage for core functionality

**Organization**: Tasks grouped by user story for independent implementation

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3)

---

## Phase 1: Setup (1 task)

**Purpose**: Install OpenAI Agents SDK dependency

- [X] T001 Add OpenAI SDK to `backend/pyproject.toml` and run `pip install openai-agents`

---

## Phase 2: Foundational (3 tasks)

**Purpose**: Database models and agent configuration - MUST complete before user stories

- [X] T002 [P] Create Conversation and Message models in `backend/src/models/conversation.py`
- [X] T003 [P] Create database migration `backend/migrations/005_add_conversation_models.sql`
- [X] T004 [P] Create agent configuration in `backend/src/agent/config.py`

---

## Phase 3: User Story 1 - Chat with AI Agent (P1) 🎯 MVP

**Goal**: Implement POST /api/{user_id}/chat endpoint with agent orchestration

**Independent Test**: Send natural language requests, verify tool invocations and task operations

- [X] T005 [P] [US1] Create chat endpoint in `backend/src/api/chat.py` (POST /api/{user_id}/chat)
- [X] T006 [US1] Create agent service in `backend/src/services/agent_service.py` (orchestrate agent + MCP tools)
- [X] T007 [US1] Implement conversation service in `backend/src/services/conversation_service.py` (get/create conversation)
- [X] T008 [US1] Integrate MCP tools with agent in `backend/src/services/agent_service.py`

**Checkpoint**: Chat endpoint functional, agent invokes MCP tools correctly

---

## Phase 4: User Story 2 - Persistent History (P2)

**Goal**: Persist all messages to database, fetch history on every request

**Independent Test**: Send multiple messages, restart server, verify history retrieval

- [X] T009 [P] [US2] Implement message persistence in `backend/src/services/conversation_service.py` (store_message function)
- [X] T010 [P] [US2] Implement history retrieval in `backend/src/services/conversation_service.py` (get_conversation_history function)
- [X] T011 [US2] Update chat endpoint to fetch history before agent execution (already in backend/src/api/chat.py)

**Checkpoint**: Conversation history persists across requests and server restarts

---

## Phase 5: User Story 3 - Tool Transparency (P3)

**Goal**: Include tool_calls in agent responses for transparency

**Independent Test**: Verify responses include tool invocation details and error handling

- [X] T012 [P] [US3] Add tool_calls capture in `backend/src/services/agent_service.py` (capture tool name, args, result)
- [X] T013 [P] [US3] Add tool_calls to Message model storage in `backend/src/models/conversation.py`
- [X] T014 [US3] Implement graceful error handling in `backend/src/services/agent_service.py` (handle NOT_FOUND, OWNERSHIP_VIOLATION)

**Checkpoint**: Agent responses include tool_calls, errors handled gracefully

---

## Phase 6: Polish (2 tasks)

**Purpose**: Documentation and API endpoints

- [X] T015 [P] Add GET /api/{user_id}/conversations endpoint in `backend/src/api/chat.py` (list user conversations)
- [X] T016 Update `backend/README.md` with chat endpoint documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP ready
- **User Story 2 (Phase 4)**: Depends on Foundational - can run parallel with US1
- **User Story 3 (Phase 5)**: Depends on US1 - adds transparency
- **Polish (Phase 6)**: Depends on all user stories

### User Story Dependencies

- **US1 (P1)**: Core chat functionality - implement first
- **US2 (P2)**: History persistence - enhances US1
- **US3 (P3)**: Tool transparency - enhances US1

### Parallel Opportunities

- **Foundational phase**: T002, T003, T004 can run in parallel
- **User Story 1**: T005, T006, T007, T008 can run in parallel (different files)
- **User Story 2**: T009, T010, T011 can run in parallel
- **User Story 3**: T012, T013, T014 can run in parallel
- **Polish phase**: T015, T016 can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002-T004)
3. Complete Phase 3: User Story 1 (T005-T008)
4. **STOP and VALIDATE**: Test chat endpoint with natural language requests
5. Deploy/demo if ready - MVP delivers AI-powered task management

### Incremental Delivery

1. Complete Setup + Foundational → Models and config ready
2. Add User Story 1 → Chat with agent, tool invocation → Deploy/Demo (MVP!)
3. Add User Story 2 → Persistent history, multi-turn conversations → Deploy/Demo
4. Add User Story 3 → Tool transparency, error handling → Deploy/Demo
5. Add Polish → Additional endpoints, documentation → Final release

---

## Task Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1: Setup | 1 | Install OpenAI SDK |
| Phase 2: Foundational | 3 | Models, migration, agent config |
| Phase 3: US1 (P1) | 4 | Chat endpoint, agent service, MCP integration |
| Phase 4: US2 (P2) | 3 | Message persistence, history retrieval |
| Phase 5: US3 (P3) | 3 | Tool capture, storage, error handling |
| Phase 6: Polish | 2 | Additional endpoints, docs |
| **Total** | **16** | Concise AI agent implementation |

### MVP Scope (User Story 1 Only)

**Minimum for MVP**: Phases 1, 2, and 3 (8 tasks)
- OpenAI Agents SDK installed
- Conversation and Message models
- Chat endpoint functional
- Agent orchestrates MCP tools
- Basic task management via natural language
- **Excludes**: Full history persistence, tool transparency (can be added later)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [US1], [US2], [US3] labels map tasks to specific user stories
- Each user story independently testable
- Commit after each task or logical group
- Chat endpoint is core - prioritize T005-T008 in US1
- Error handling critical for production - do not skip T014
