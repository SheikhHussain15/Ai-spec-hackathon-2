# API Contract: Task Management Endpoints

## GET /api/tasks/{user_id}/tasks
**Purpose**: Retrieve all tasks for the specified user

### Request
- **Method**: GET
- **Path**: `/api/tasks/{user_id}/tasks`
- **Headers**: 
  - Authorization: Bearer {JWT_TOKEN}
- **Path Parameters**:
  - user_id: The ID of the user whose tasks to retrieve
- **Query Parameters**: None
- **Body**: None
- **Validation**:
  - JWT must be valid and unexpired
  - user_id in path must match user_id in JWT claims

### Response
- **Success (200)**:
  ```json
  [
    {
      "id": "task-uuid-string",
      "title": "Sample task",
      "description": "Task description",
      "completed": false,
      "user_id": "user-uuid-string",
      "created_at": "2026-02-09T10:00:00Z",
      "updated_at": "2026-02-09T10:00:00Z"
    }
  ]
  ```
- **Failure (401)**:
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- **Failure (403)**:
  ```json
  {
    "detail": "Access denied: user ID mismatch"
  }
  ```

---

## POST /api/tasks/{user_id}/tasks
**Purpose**: Create a new task for the specified user

### Request
- **Method**: POST
- **Path**: `/api/tasks/{user_id}/tasks`
- **Headers**: 
  - Authorization: Bearer {JWT_TOKEN}
  - Content-Type: application/json
- **Path Parameters**:
  - user_id: The ID of the user creating the task
- **Body**:
  ```json
  {
    "title": "New task",
    "description": "Task description",
    "completed": false
  }
  ```
- **Validation**:
  - JWT must be valid and unexpired
  - user_id in path must match user_id in JWT claims
  - Title must be provided and not empty

### Response
- **Success (201)**:
  ```json
  {
    "id": "task-uuid-string",
    "title": "New task",
    "description": "Task description",
    "completed": false,
    "user_id": "user-uuid-string",
    "created_at": "2026-02-09T10:00:00Z",
    "updated_at": "2026-02-09T10:00:00Z"
  }
  ```
- **Failure (400)**:
  ```json
  {
    "detail": "Validation error"
  }
  ```
- **Failure (401)**:
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- **Failure (403)**:
  ```json
  {
    "detail": "Access denied: user ID mismatch"
  }
  ```

---

## GET /api/tasks/{user_id}/tasks/{task_id}
**Purpose**: Retrieve a specific task for the specified user

### Request
- **Method**: GET
- **Path**: `/api/tasks/{user_id}/tasks/{task_id}`
- **Headers**: 
  - Authorization: Bearer {JWT_TOKEN}
- **Path Parameters**:
  - user_id: The ID of the user whose task to retrieve
  - task_id: The ID of the specific task to retrieve
- **Validation**:
  - JWT must be valid and unexpired
  - user_id in path must match user_id in JWT claims
  - Task must exist and belong to the specified user

### Response
- **Success (200)**:
  ```json
  {
    "id": "task-uuid-string",
    "title": "Sample task",
    "description": "Task description",
    "completed": false,
    "user_id": "user-uuid-string",
    "created_at": "2026-02-09T10:00:00Z",
    "updated_at": "2026-02-09T10:00:00Z"
  }
  ```
- **Failure (401)**:
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- **Failure (403)**:
  ```json
  {
    "detail": "Access denied: user ID mismatch"
  }
  ```
- **Failure (404)**:
  ```json
  {
    "detail": "Task not found"
  }
  ```

---

## PUT /api/tasks/{user_id}/tasks/{task_id}
**Purpose**: Update a specific task for the specified user

### Request
- **Method**: PUT
- **Path**: `/api/tasks/{user_id}/tasks/{task_id}`
- **Headers**: 
  - Authorization: Bearer {JWT_TOKEN}
  - Content-Type: application/json
- **Path Parameters**:
  - user_id: The ID of the user whose task to update
  - task_id: The ID of the specific task to update
- **Body**:
  ```json
  {
    "title": "Updated task",
    "description": "Updated description",
    "completed": true
  }
  ```
- **Validation**:
  - JWT must be valid and unexpired
  - user_id in path must match user_id in JWT claims
  - Task must exist and belong to the specified user

### Response
- **Success (200)**:
  ```json
  {
    "id": "task-uuid-string",
    "title": "Updated task",
    "description": "Updated description",
    "completed": true,
    "user_id": "user-uuid-string",
    "created_at": "2026-02-09T10:00:00Z",
    "updated_at": "2026-02-09T11:00:00Z"
  }
  ```
- **Failure (400)**:
  ```json
  {
    "detail": "Validation error"
  }
  ```
- **Failure (401)**:
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- **Failure (403)**:
  ```json
  {
    "detail": "Access denied: user ID mismatch"
  }
  ```
- **Failure (404)**:
  ```json
  {
    "detail": "Task not found"
  }
  ```

---

## PATCH /api/tasks/{user_id}/tasks/{task_id}/complete
**Purpose**: Update only the completion status of a specific task for the specified user

### Request
- **Method**: PATCH
- **Path**: `/api/tasks/{user_id}/tasks/{task_id}/complete`
- **Headers**: 
  - Authorization: Bearer {JWT_TOKEN}
  - Content-Type: application/json
- **Path Parameters**:
  - user_id: The ID of the user whose task to update
  - task_id: The ID of the specific task to update
- **Body**:
  ```json
  {
    "completed": true
  }
  ```
- **Validation**:
  - JWT must be valid and unexpired
  - user_id in path must match user_id in JWT claims
  - Task must exist and belong to the specified user

### Response
- **Success (200)**:
  ```json
  {
    "id": "task-uuid-string",
    "title": "Sample task",
    "description": "Task description",
    "completed": true,
    "user_id": "user-uuid-string",
    "created_at": "2026-02-09T10:00:00Z",
    "updated_at": "2026-02-09T11:00:00Z"
  }
  ```
- **Failure (400)**:
  ```json
  {
    "detail": "Validation error"
  }
  ```
- **Failure (401)**:
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- **Failure (403)**:
  ```json
  {
    "detail": "Access denied: user ID mismatch"
  }
  ```
- **Failure (404)**:
  ```json
  {
    "detail": "Task not found"
  }
  ```

---

## DELETE /api/tasks/{user_id}/tasks/{task_id}
**Purpose**: Delete a specific task for the specified user

### Request
- **Method**: DELETE
- **Path**: `/api/tasks/{user_id}/tasks/{task_id}`
- **Headers**: 
  - Authorization: Bearer {JWT_TOKEN}
- **Path Parameters**:
  - user_id: The ID of the user whose task to delete
  - task_id: The ID of the specific task to delete
- **Validation**:
  - JWT must be valid and unexpired
  - user_id in path must match user_id in JWT claims
  - Task must exist and belong to the specified user

### Response
- **Success (204)**: Empty response body
- **Failure (401)**:
  ```json
  {
    "detail": "Could not validate credentials"
  }
  ```
- **Failure (403)**:
  ```json
  {
    "detail": "Access denied: user ID mismatch"
  }
  ```
- **Failure (404)**:
  ```json
  {
    "detail": "Task not found"
  }
  ```