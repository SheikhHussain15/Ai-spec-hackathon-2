# Tasks: In-memory Todo Console Application

**Input**: Design documents from `specs/001-in-memory-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md

**Tests**: Unit tests are included for core business logic.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directories `src` and `tests`
- [x] T002 [P] Create empty file `src/models.py`
- [x] T003 [P] Create empty file `src/services.py`
- [x] T004 [P] Create empty file `src/main.py`
- [x] T005 [P] Create empty file `src/validation.py`
- [x] T006 [P] Create empty file `tests/test_services.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data model that MUST be complete before ANY user story can be implemented

- [x] T007 Implement the `Task` data class in `src/models.py`

---

## Phase 3: User Story 1 - Add a new task (Priority: P1) 🎯 MVP

**Goal**: Allows a user to add a new task to the to-do list.

**Independent Test**: Run the application, choose the "add" option, enter a task description, and verify the task is added by viewing the list.

### Implementation for User Story 1

- [x] T008 [US1] Implement `add_task` function in `src/services.py`
- [x] T009 [US1] Implement the `add_task` command in `src/main.py`
- [x] T010 [US1] Add a unit test for `add_task` in `tests/test_services.py`

---

## Phase 4: User Story 2 - View all tasks (Priority: P1)

**Goal**: Allows a user to see all the tasks in the to-do list.

**Independent Test**: Add several tasks and verify they are all displayed correctly when choosing the "view" option.

### Implementation for User Story 2

- [x] T011 [US2] Implement `view_tasks` function in `src/services.py`
- [x] T012 [US2] Implement the `view_tasks` command in `src/main.py`

---

## Phase 5: User Story 3 - Update a task (Priority: P2)

**Goal**: Allows a user to update the description of an existing task.

**Independent Test**: Add a task, then use the "update" option to change its description, and verify the change by viewing the list.

### Implementation for User Story 3

- [x] T013 [US3] Implement `update_task` function in `src/services.py`
- [x] T014 [US3] Implement the `update_task` command in `src/main.py`
- [x] T015 [US3] Add a unit test for `update_task` in `tests/test_services.py`

---

## Phase 6: User Story 4 - Mark a task as complete (Priority: P2)

**Goal**: Allows a user to mark a task as complete.

**Independent Test**: Add a task, use the "mark complete" option, and verify the task's status is updated.

### Implementation for User Story 4

- [x] T016 [US4] Implement `mark_task_complete` function in `src/services.py`
- [x] T017 [US4] Implement the `mark_task_complete` command in `src/main.py`
- [x] T018 [US4] Add a unit test for `mark_task_complete` in `tests/test_services.py`

---

## Phase 7: User Story 5 - Delete a task (Priority: P3)

**Goal**: Allows a user to delete a task from the to-do list.

**Independent Test**: Add a task, then use the "delete" option, and verify the task is removed from the list.

### Implementation for User Story 5

- [x] T019 [US5] Implement `delete_task` function in `src/services.py`
- [x] T020 [US5] Implement the `delete_task` command in `src/main.py`
- [x] T021 [US5] Add a unit test for `delete_task` in `tests/test_services.py`

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final integration, UI, and error handling.

- [x] T022 Implement the main application loop and menu in `src/main.py`
- [x] T023 Implement input validation functions in `src/validation.py`
- [x] T024 Integrate validation and error handling in `src/main.py`

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** must complete before all other phases.
- **Phase 2 (Foundational)** depends on Phase 1.
- **Phases 3-7 (User Stories)** depend on Phase 2. They can be implemented in priority order or in parallel.
- **Phase 8 (Polish)** depends on all user story phases.

## Implementation Strategy

### MVP First (User Story 1 & 2)

1.  Complete Phase 1 & 2.
2.  Complete Phase 3 (Add Task) and Phase 4 (View Tasks).
3.  **STOP and VALIDATE**: Test adding and viewing tasks. This is the core MVP.

### Incremental Delivery

1.  Deliver MVP.
2.  Add User Story 3 (Update).
3.  Add User Story 4 (Mark Complete).
4.  Add User Story 5 (Delete).
5.  Complete Phase 8 (Polish).
