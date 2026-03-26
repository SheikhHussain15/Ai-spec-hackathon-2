# Implementation Plan: Chat UI (ChatKit Integration)

**Branch**: `006-chat-ui` | **Date**: 2026-02-18 | **Spec**: [specs/006-chat-ui/spec.md](../spec.md)
**Input**: Feature specification from `/specs/006-chat-ui/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a conversational chat UI using React and Next.js App Router that integrates with the AI agent backend. Implement protected chat page, conversation state management, message rendering with user/assistant distinction, and graceful handling of loading/error/empty states. All state persists through localStorage for conversation ID only—no sensitive data stored in frontend.

## Technical Context

**Language/Version**: TypeScript 5+, React 18, Next.js 14
**Primary Dependencies**: OpenAI SDK (for types), Axios (HTTP client), clsx (utility)
**Storage**: localStorage for conversation_id persistence only
**Testing**: React Testing Library, Jest (if tests requested)
**Target Platform**: Web (mobile-first responsive design)
**Project Type**: Frontend (Next.js App Router)
**Performance Goals**: Message rendering <100ms, API response <5s p95
**Constraints**: No sensitive data in browser, JWT from auth context, no streaming
**Scale/Scope**: Single-user chat interface with conversation history

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

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

### Operational Constraints Compliance
- [x] Architecture will be compatible with serverless deployment
- [x] No background workers will be used
- [x] No hidden state between requests
- [x] No direct frontend-to-MCP calls (backend orchestration only)

### Frontend Standards Compliance
- [x] Auth-aware routing (protected chat page)
- [x] JWT attached automatically to all API requests
- [x] Clear UX feedback for loading, errors, and auth failures
- [x] Responsive and accessible UI

**GATE RESULT**: All compliance items checked - proceeding to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/006-chat-ui/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── chat-api.json        # Chat endpoint API contract
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (frontend root)

```text
frontend/
├── app/
│   └── chat/
│       └── page.tsx         # Protected chat page
├── src/
│   ├── components/
│   │   └── chat/
│   │       ├── ChatMessage.tsx    # Message bubble component
│   │       ├── ChatInput.tsx      # Input component
│   │       ├── ChatLoading.tsx    # Loading indicator
│   │       ├── ChatError.tsx      # Error state component
│   │       └── ChatEmptyState.tsx # Empty state component
│   ├── hooks/
│   │   └── useChat.ts         # Chat state management hook
│   └── lib/
│       ├── auth.ts            # JWT utilities
│       └── storage.ts         # localStorage utilities
└── tests/
    └── components/
        └── chat/              # Component tests (if requested)
```

**Structure Decision**: Using existing `frontend/` structure from Phase-3. Chat components are new module under `frontend/src/components/chat/`. State management via custom React hook `useChat`.

## Complexity Tracking

All constitution compliance items pass - no complexity justification needed.

## Phase 0: Research Plan

### Research Tasks

1. **Next.js App Router Chat Page**
   - Research protected route patterns in Next.js App Router
   - Document authentication redirect patterns
   - Identify client vs server component considerations

2. **Conversation State Management**
   - Research React hook patterns for chat state
   - Document localStorage best practices for conversation_id
   - Identify auto-scroll patterns for message lists

3. **Message Rendering Patterns**
   - Research chat UI component patterns (user vs assistant bubbles)
   - Document animation patterns for message entry
   - Identify tool call display patterns

4. **API Integration**
   - Research JWT attachment patterns for fetch/axios
   - Document error handling patterns for chat APIs
   - Identify loading state management patterns

## Phase 1: Design Deliverables

### contracts/
- `chat-api.json`: Chat endpoint request/response OpenAPI schema

### quickstart.md
- Chat page setup instructions
- Component structure guide
- State management explanation
- Testing instructions

### research.md
- Next.js App Router patterns
- Conversation state management approach
- Message rendering patterns
- API integration strategy

## Next Steps

After this plan is complete, the next phase is `/sp.tasks` to break this implementation into actionable tasks.
