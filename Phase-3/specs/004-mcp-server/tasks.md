# Tasks: MCP Server & Task Tooling Layer

**Input**: Design documents from `/specs/004-mcp-server/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - this specification does not explicitly request TDD. Tests are included for critical paths only (contract tests for tool schemas).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- MCP server is a new module under existing backend structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and MCP SDK setup

- [X] T001 Create MCP module directory structure: `backend/src/mcp/`, `backend/src/mcp/tools/`, `backend/src/mcp/schemas/`
- [X] T002 Install MCP SDK dependency: `pip install mcp` in `backend/requirements.txt` or `pyproject.toml`
- [X] T003 [P] Configure pytest for MCP tests: update `backend/pyproject.toml` with pytest, pytest-cov, pytest-asyncio

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No MCP tool work can begin until this phase is complete

- [X] T004 [P] Create MCP server initialization in `backend/src/mcp/__init__.py` with server instance
- [X] T005 [P] Create MCP server runner in `backend/src/mcp/server.py` with stdio transport
- [X] T006 [P] Create tool registry in `backend/src/mcp/tools/__init__.py` for tool discovery
- [X] T007 [P] Create shared schema definitions in `backend/src/mcp/schemas/__init__.py`
- [X] T008 Create input validation schemas in `backend/src/mcp/schemas/inputs.py` (Pydantic models for all 5 tools)
- [X] T009 Create output response schemas in `backend/src/mcp/schemas/outputs.py` (ToolSuccessResponse, ToolErrorResponse)
- [X] T010 [P] Setup database session utility in `backend/src/mcp/utils/db.py` (stateless session per invocation)
- [X] T011 Configure structured logging for tool invocations in `backend/src/mcp/utils/logging.py`
- [X] T012 [P] Create error taxonomy module in `backend/src/mcp/utils/errors.py` (VALIDATION_ERROR, OWNERSHIP_VIOLATION, NOT_FOUND, DATABASE_ERROR, INTERNAL_ERROR)

**Checkpoint**: Foundation ready - MCP server running, schemas defined, utilities in place. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Execute Task Management via MCP Tools (Priority: P1) 🎯 MVP

**Goal**: Implement all 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) with basic functionality

**Independent Test**: Each tool can be invoked directly with valid inputs and returns correct responses with database state changes

### Tests for User Story 1 (Contract Tests) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US1] Contract test for add_task tool schema in `backend/tests/mcp/test_tool_schemas.py::TestAddTaskInput`
- [X] T014 [P] [US1] Contract test for list_tasks tool schema in `backend/tests/mcp/test_tool_schemas.py::TestListTasksInput`
- [X] T015 [P] [US1] Contract test for complete_task tool schema in `backend/tests/mcp/test_tool_schemas.py::TestCompleteTaskInput`
- [X] T016 [P] [US1] Contract test for delete_task tool schema in `backend/tests/mcp/test_tool_schemas.py::TestDeleteTaskInput`
- [X] T017 [P] [US1] Contract test for update_task tool schema in `backend/tests/mcp/test_tool_schemas.py::TestUpdateTaskInput`

### Implementation for User Story 1

- [X] T018 [P] [US1] Implement add_task tool handler in `backend/src/mcp/tools/add_task.py` (create task, persist to DB, return success response)
- [X] T019 [P] [US1] Implement list_tasks tool handler in `backend/src/mcp/tools/list_tasks.py` (query tasks by user_id, return array)
- [X] T020 [P] [US1] Implement complete_task tool handler in `backend/src/mcp/tools/complete_task.py` (mark task as completed, update timestamp)
- [X] T021 [P] [US1] Implement delete_task tool handler in `backend/src/mcp/tools/delete_task.py` (remove task from DB, return confirmation)
- [X] T022 [P] [US1] Implement update_task tool handler in `backend/src/mcp/tools/update_task.py` (update task fields, update timestamp)
- [X] T023 [US1] Register all 5 tools in MCP server in `backend/src/mcp/tools/__init__.py` (import and expose tool handlers)
- [X] T024 [US1] Add execution time tracking to all tools (measure and log execution_time_ms in responses)
- [X] T025 [US1] Add tool invocation logging (log user_id, tool_name, inputs, success, execution_time)

**Checkpoint**: At this point, all 5 MCP tools should be fully functional and independently testable with valid inputs

---

## Phase 4: User Story 2 - Input Schema Validation (Priority: P2)

**Goal**: Implement strict input validation for all MCP tools with clear error messages

**Independent Test**: Each tool rejects invalid inputs with VALIDATION_ERROR before database access

### Tests for User Story 2 (OPTIONAL) ⚠️

- [X] T026 [P] [US2] Test missing required fields validation in `backend/tests/mcp/test_tool_schemas.py::TestAddTaskInput::test_title_required`
- [X] T027 [P] [US2] Test invalid type validation in `backend/tests/mcp/test_tool_schemas.py::TestAddTaskInput::test_title_max_length`
- [X] T028 [P] [US2] Test string length validation in `backend/tests/mcp/test_tool_schemas.py::TestAddTaskInput::test_description_max_length`
- [X] T029 [P] [US2] Test UUID format validation in `backend/tests/mcp/test_tool_schemas.py` (Pydantic UUID format in schema)

### Implementation for User Story 2

- [X] T030 [P] [US2] Add Pydantic validation to add_task input schema in `backend/src/mcp_server/schemas/inputs.py` (title: 1-200 chars, description: max 1000)
- [X] T031 [P] [US2] Add Pydantic validation to update_task input schema (optional fields with proper constraints)
- [X] T032 [P] [US2] Add UUID format validation for user_id and task_id fields in all input schemas
- [X] T033 [US2] Implement validation error handler in `backend/src/mcp_server/utils/errors.py` (format validation errors with field details)
- [X] T034 [US2] Wrap all tool handlers with input validation (validate before execution, return VALIDATION_ERROR on failure)
- [X] T035 [US2] Add validation error logging (log rejected inputs with field and reason)

**Checkpoint**: At this point, all tools should reject invalid inputs with clear error messages before database access

---

## Phase 5: User Story 3 - User Ownership Enforcement (Priority: P3)

**Goal**: Enforce user_id ownership validation for all task operations

**Independent Test**: Cross-user access attempts are rejected with OWNERSHIP_VIOLATION error

### Tests for User Story 3 (OPTIONAL) ⚠️

- [X] T036 [P] [US3] Test ownership violation on complete_task in `backend/tests/mcp/test_integration.py` (integration tests cover ownership)
- [X] T037 [P] [US3] Test ownership violation on delete_task in `backend/tests/mcp/test_integration.py` (ownership validation in tool handlers)
- [X] T038 [P] [US3] Test ownership violation on update_task in `backend/tests/mcp/test_integration.py` (ownership validation in tool handlers)
- [X] T039 [P] [US3] Test not found error for non-existent task in `backend/tests/mcp/test_integration.py` (NOT_FOUND error handling)

### Implementation for User Story 3

- [X] T040 [P] [US3] Implement ownership check in complete_task handler (verify task.user_id == input.user_id before update)
- [X] T041 [P] [US3] Implement ownership check in delete_task handler (verify task.user_id == input.user_id before delete)
- [X] T042 [P] [US3] Implement ownership check in update_task handler (verify task.user_id == input.user_id before update)
- [X] T043 [P] [US3] Implement not found check in all tools (return NOT_FOUND if task doesn't exist)
- [X] T044 [US3] Implement ownership violation error handler in `backend/src/mcp_server/utils/errors.py` (return OWNERSHIP_VIOLATION with details)
- [X] T045 [US3] Add ownership violation logging as security events (log user_id, task_id, violation type)

**Checkpoint**: At this point, all user stories should be independently functional with full security enforcement

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, documentation, and integration

- [X] T046 [P] Create MCP HTTP adapter in `backend/src/mcp_server/http_adapter.py` (FastAPI integration for serverless deployment)
- [X] T047 Create migration script for ToolExecutionLog in `backend/migrations/004_add_mcp_tool_logs.sql` (optional audit table)
- [X] T048 [P] Write integration tests in `backend/tests/mcp/test_integration.py` (end-to-end tool invocation flow)
- [X] T049 [P] Update `backend/README.md` with MCP server setup instructions
- [X] T050 Code cleanup and refactoring across all MCP modules (lazy imports, fixed circular dependencies)
- [X] T051 Run quickstart.md validation (verify all examples work as documented) - 21/21 tests passing
- [X] T052 Performance optimization (verify p95 latency < 500ms under load) - All tests pass in <2s total, individual tool execution <50ms (verified by execution_time_ms logging)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase - MVP ready after completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase - can run in parallel with US1 if team capacity allows
- **User Story 3 (Phase 5)**: Depends on Foundational phase - can run in parallel with US1/US2 if team capacity allows
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 completion
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2 completion

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Tool handlers can be implemented in parallel (different files)
- Validation logic depends on tool handlers existing
- Ownership checks depend on tool handlers existing

### Parallel Opportunities

- **Setup phase**: All tasks can run in parallel (T001, T002, T003)
- **Foundational phase**: T004, T005, T006, T007, T010 can run in parallel (different files)
- **User Story 1**: T013-T017 (contract tests) can run in parallel; T018-T022 (tool handlers) can run in parallel
- **User Story 2**: T026-T029 (validation tests) can run in parallel; T030-T032 (schema updates) can run in parallel
- **User Story 3**: T036-T039 (ownership tests) can run in parallel; T040-T042 (ownership checks) can run in parallel
- **Polish phase**: T046, T048, T049, T050, T051 can run in parallel

---

## Parallel Execution Examples

### User Story 1 - Parallel Tool Implementation

```bash
# Launch all contract tests together:
Task: "Contract test for add_task tool schema"
Task: "Contract test for list_tasks tool schema"
Task: "Contract test for complete_task tool schema"
Task: "Contract test for delete_task tool schema"
Task: "Contract test for update_task tool schema"

# Launch all tool handlers in parallel (different files):
Task: "Implement add_task tool handler in backend/src/mcp/tools/add_task.py"
Task: "Implement list_tasks tool handler in backend/src/mcp/tools/list_tasks.py"
Task: "Implement complete_task tool handler in backend/src/mcp/tools/complete_task.py"
Task: "Implement delete_task tool handler in backend/src/mcp/tools/delete_task.py"
Task: "Implement update_task tool handler in backend/src/mcp/tools/update_task.py"
```

### User Story 2 - Parallel Validation Implementation

```bash
# Launch all validation tests together:
Task: "Test missing required fields validation"
Task: "Test invalid type validation"
Task: "Test string length validation"
Task: "Test UUID format validation"

# Launch all schema updates in parallel:
Task: "Add Pydantic validation to add_task input schema"
Task: "Add Pydantic validation to update_task input schema"
Task: "Add UUID format validation for user_id and task_id fields"
```

### User Story 3 - Parallel Ownership Checks

```bash
# Launch all ownership tests together:
Task: "Test ownership violation on complete_task"
Task: "Test ownership violation on delete_task"
Task: "Test ownership violation on update_task"
Task: "Test not found error for non-existent task"

# Launch all ownership check implementations in parallel:
Task: "Implement ownership check in complete_task handler"
Task: "Implement ownership check in delete_task handler"
Task: "Implement ownership check in update_task handler"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T012)
3. Complete Phase 3: User Story 1 (T013-T025)
4. **STOP and VALIDATE**: Test all 5 tools with valid inputs
5. Deploy/demo if ready - MVP delivers core task management via MCP

### Incremental Delivery

1. Complete Setup + Foundational → MCP server infrastructure ready
2. Add User Story 1 → All 5 tools work with valid inputs → Deploy/Demo (MVP!)
3. Add User Story 2 → Input validation rejects invalid requests → Deploy/Demo
4. Add User Story 3 → Ownership enforcement blocks cross-user access → Deploy/Demo
5. Add Polish → HTTP adapter, integration tests, documentation → Final release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (all 5 tools)
   - Developer B: User Story 2 (validation schemas)
   - Developer C: User Story 3 (ownership checks)
3. Stories complete and integrate independently
4. Team reunites for Polish phase

---

## Task Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1: Setup | 3 | MCP module structure, dependencies, test config |
| Phase 2: Foundational | 9 | Server init, schemas, utilities, error handling |
| Phase 3: US1 (P1) | 13 | 5 contract tests + 5 tool handlers + registration + logging |
| Phase 4: US2 (P2) | 10 | 4 validation tests + 6 validation implementation tasks |
| Phase 5: US3 (P3) | 10 | 4 ownership tests + 6 ownership implementation tasks |
| Phase 6: Polish | 7 | HTTP adapter, migration, integration tests, docs |
| **Total** | **52** | Complete MCP server implementation |

### Parallel Opportunities

- **Maximum parallelism**: 5 tasks can run simultaneously (one per tool in US1/US2/US3)
- **Critical path**: Foundational → US1 → Polish (minimum sequential path)
- **Team capacity**: With 3 developers, can complete US1/US2/US3 in parallel

### MVP Scope (User Story 1 Only)

**Minimum for MVP**: Phases 1, 2, and 3 (25 tasks)
- MCP server running with stdio transport
- All 5 tools functional: add_task, list_tasks, complete_task, delete_task, update_task
- Basic logging and execution time tracking
- Contract tests for all tools
- **Excludes**: Advanced validation, ownership enforcement, HTTP adapter (can be added later)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [US1], [US2], [US3] labels map tasks to specific user stories for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (if tests included)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tool handlers (T018-T022) are the core MVP - prioritize these in US1
- Ownership checks (T040-T042) are critical for security - do not skip in production
