# Tasks: Chat UI (ChatKit Integration)

**Input**: Design documents from `/specs/006-chat-ui/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, contracts/

**Tests**: Optional - minimal test coverage for core functionality

**Organization**: Tasks grouped by user story for independent implementation

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3)

---

## Phase 1: Setup (2 tasks)

**Purpose**: Install dependencies and create base structure

- [X] T001 [P] Install chat UI dependencies: `npm install openai clsx` in frontend
- [X] T002 [P] Create chat page directory in `frontend/app/chat/`

---

## Phase 2: User Story 1 - Chat with AI Agent (P1) 🎯 MVP

**Goal**: Implement functional chat UI with message rendering

**Independent Test**: Send messages, verify they render with user/assistant distinction

- [X] T003 [P] [US1] Create ChatMessage component in `frontend/src/components/chat/ChatMessage.tsx`
- [X] T004 [P] [US1] Create ChatInput component in `frontend/src/components/chat/ChatInput.tsx`
- [X] T005 [US1] Implement chat page in `frontend/app/chat/page.tsx`
- [X] T006 [US1] Add JWT authentication to chat API requests in `frontend/src/lib/auth.ts`

**Checkpoint**: Chat UI functional, messages render correctly

---

## Phase 3: User Story 2 - Conversation Persistence (P2)

**Goal**: Persist conversation_id and restore history

**Independent Test**: Refresh page, verify conversation history restored

- [X] T007 [P] [US2] Implement useChat hook in `frontend/src/hooks/useChat.ts`
- [X] T008 [P] [US2] Add conversation_id persistence in `frontend/src/lib/storage.ts`
- [X] T009 [US2] Fetch conversation history on page load in `frontend/app/chat/page.tsx`

**Checkpoint**: Conversations persist across page refreshes

---

## Phase 4: User Story 3 - Loading/Error/Empty States (P3)

**Goal**: Graceful state handling

**Independent Test**: Trigger loading/error/empty states, verify UI handles gracefully

- [X] T010 [P] [US3] Add loading indicator in `frontend/src/components/chat/ChatLoading.tsx`
- [X] T011 [P] [US3] Add error handling with retry in `frontend/src/components/chat/ChatError.tsx`
- [X] T012 [US3] Add empty state for new users in `frontend/src/components/chat/ChatEmptyState.tsx`

**Checkpoint**: All states handled gracefully

---

## Phase 5: Polish (3 tasks)

**Purpose**: Animations, responsiveness, documentation

- [X] T013 [P] Add smooth message animations in `frontend/src/components/chat/ChatMessage.tsx` (via globals.css)
- [X] T014 [P] Add auto-scroll behavior in `frontend/app/chat/page.tsx` (via useChat hook)
- [X] T015 Update `frontend/README.md` with chat UI documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup - MVP ready after completion
- **User Story 2 (Phase 3)**: Depends on Setup - can run parallel with US1 if team capacity allows
- **User Story 3 (Phase 4)**: Depends on Setup - can run parallel with US1/US2
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Setup - No dependencies on other stories
- **US2 (P2)**: Can start after Setup - Independent of US1 completion
- **US3 (P3)**: Can start after Setup - Independent of US1/US2 completion

### Within Each User Story

- Components can be implemented in parallel (different files)
- Page integration depends on components existing
- State management depends on components existing

### Parallel Opportunities

- **Setup phase**: T001, T002 can run in parallel
- **User Story 1**: T003, T004 can run in parallel (different components)
- **User Story 2**: T007, T008 can run in parallel (hook + storage)
- **User Story 3**: T010, T011, T012 can run in parallel (different components)
- **Polish phase**: T013, T014 can run in parallel

---

## Parallel Execution Examples

### User Story 1 - Parallel Component Implementation

```bash
# Launch all components together:
Task: "Create ChatMessage component in frontend/src/components/chat/ChatMessage.tsx"
Task: "Create ChatInput component in frontend/src/components/chat/ChatInput.tsx"

# Then integrate:
Task: "Implement chat page in frontend/app/chat/page.tsx"
```

### User Story 2 - Parallel State Management

```bash
# Launch state management tasks together:
Task: "Implement useChat hook in frontend/src/hooks/useChat.ts"
Task: "Add conversation_id persistence in frontend/src/lib/storage.ts"

# Then integrate:
Task: "Fetch conversation history on page load in frontend/app/chat/page.tsx"
```

### User Story 3 - Parallel State Components

```bash
# Launch all state components together:
Task: "Add loading indicator in frontend/src/components/chat/ChatLoading.tsx"
Task: "Add error handling with retry in frontend/src/components/chat/ChatError.tsx"
Task: "Add empty state for new users in frontend/src/components/chat/ChatEmptyState.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: User Story 1 (T003-T006)
3. **STOP and VALIDATE**: Test chat UI with message sending
4. Deploy/demo if ready - MVP delivers functional chat interface

### Incremental Delivery

1. Complete Setup → Chat page structure ready
2. Add User Story 1 → Chat UI functional, messages render → Deploy/Demo (MVP!)
3. Add User Story 2 → Conversation persistence, history restore → Deploy/Demo
4. Add User Story 3 → Loading, error, empty states → Deploy/Demo
5. Add Polish → Animations, auto-scroll, documentation → Final release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup together
2. Once Setup is done:
   - Developer A: User Story 1 (chat page, components)
   - Developer B: User Story 2 (state management, persistence)
   - Developer C: User Story 3 (state components)
3. Stories complete and integrate independently
4. Team reunites for Polish phase

---

## Task Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1: Setup | 2 | Dependencies, base structure |
| Phase 2: US1 (P1) | 4 | Chat UI, message rendering, JWT |
| Phase 3: US2 (P2) | 3 | Conversation persistence, history |
| Phase 4: US3 (P3) | 3 | Loading, error, empty states |
| Phase 5: Polish | 3 | Animations, auto-scroll, docs |
| **Total** | **15** | Concise Chat UI implementation |

### Parallel Opportunities

- **Maximum parallelism**: 3 tasks can run simultaneously (different components)
- **Critical path**: Setup → US1 → Polish (minimum sequential path)
- **Team capacity**: With 3 developers, can complete US1/US2/US3 in parallel

### MVP Scope (User Story 1 Only)

**Minimum for MVP**: Phases 1 and 2 (6 tasks)
- Chat page with message list
- ChatMessage and ChatInput components
- JWT authentication
- Basic message rendering
- **Excludes**: Persistence, advanced states, animations (can be added later)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [US1], [US2], [US3] labels map tasks to specific user stories
- Each user story independently testable
- Commit after each task or logical group
- Chat UI is core - prioritize T003-T006 in US1
- State components are polish - can be added after MVP
