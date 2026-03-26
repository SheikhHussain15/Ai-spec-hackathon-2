# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Deterministic Tool Execution Compliance
- [ ] AI will plan actions explicitly before tool execution
- [ ] All tool invocations will be logged and traceable
- [ ] No autonomous behavior outside defined tool schemas

### Stateless Server Architecture Compliance
- [ ] Server will hold zero runtime conversation state
- [ ] All state will persist through database only
- [ ] Every request will fetch conversation history from database
- [ ] Server restart will not affect conversation continuity

### Clear Separation of Concerns Compliance
- [ ] UI layer will be isolated from Agent logic
- [ ] Agent layer will be isolated from MCP tools
- [ ] Backend orchestration only—no direct frontend-to-MCP calls

### Security and User Isolation Compliance
- [ ] All chat endpoints will require valid JWT authentication
- [ ] Agent will operate only within authenticated user context
- [ ] MCP tools will validate user_id before executing
- [ ] No cross-user data exposure under any condition

### Spec-Driven Agentic Development Compliance
- [ ] Development will follow spec → plan → tasks → implementation workflow
- [ ] No manual coding will be performed
- [ ] All code will be generated via Qwen Code using specialized agents

### AI Architecture Standards Compliance
- [ ] AI logic will use OpenAI Agents SDK exclusively
- [ ] All task operations will be executed via MCP tools
- [ ] No direct database access from agent
- [ ] MCP tools will be stateless and persist state only through database
- [ ] Tool schemas will be strictly validated before execution

### Backend Standards Compliance
- [ ] Chat endpoint will be: POST /api/{user_id}/chat
- [ ] Server will fetch conversation history from database on every request
- [ ] Server will store user and assistant messages persistently
- [ ] All operations will respect authenticated user isolation

### Database Standards Compliance
- [ ] Task model will be reused from Phase-2
- [ ] New models: Conversation and Message will be created
- [ ] All records will be scoped by user_id
- [ ] Conversation will resume correctly after server restart

### Security Standards Compliance
- [ ] All chat endpoints will require valid JWT
- [ ] JWT will be verified using shared secret (BETTER_AUTH_SECRET)
- [ ] User identity will be derived from JWT claims only
- [ ] Invalid, missing, or expired tokens will return 401 Unauthorized
- [ ] No hardcoded secrets or credentials in source code

### Operational Constraints Compliance
- [ ] Architecture will be compatible with serverless deployment
- [ ] No background workers will be used
- [ ] No hidden state between requests
- [ ] No direct frontend-to-MCP calls (backend orchestration only)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
