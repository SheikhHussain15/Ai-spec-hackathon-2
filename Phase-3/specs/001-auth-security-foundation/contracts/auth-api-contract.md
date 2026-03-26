# API Contract: User Authentication Endpoints

## POST /api/auth/login
**Purpose**: Authenticate user credentials and return JWT

### Request
- **Method**: POST
- **Path**: `/api/auth/login`
- **Headers**: 
  - Content-Type: application/json
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123"
  }
  ```
- **Validation**:
  - Email must be valid format
  - Password must be provided

### Response
- **Success (200)**:
  ```json
  {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "user-uuid-string",
      "email": "user@example.com"
    }
  }
  ```
- **Failure (401)**:
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

---

## POST /api/auth/register
**Purpose**: Register new user account and return JWT

### Request
- **Method**: POST
- **Path**: `/api/auth/register`
- **Headers**: 
  - Content-Type: application/json
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123"
  }
  ```
- **Validation**:
  - Email must be valid format and unique
  - Password must meet security requirements

### Response
- **Success (201)**:
  ```json
  {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "user-uuid-string",
      "email": "user@example.com"
    }
  }
  ```
- **Failure (400)**:
  ```json
  {
    "error": "Invalid input or email already exists"
  }
  ```

---

## GET /api/users/{user_id}/tasks
**Purpose**: Retrieve tasks for the authenticated user

### Request
- **Method**: GET
- **Path**: `/api/users/{user_id}/tasks`
- **Headers**: 
  - Authorization: Bearer {JWT_TOKEN}
- **Path Parameters**:
  - user_id: The ID of the user whose tasks to retrieve
- **Validation**:
  - JWT must be valid and unexpired
  - user_id in path must match user_id in JWT claims

### Response
- **Success (200)**:
  ```json
  {
    "tasks": [
      {
        "id": "task-uuid-string",
        "title": "Sample task",
        "description": "Task description",
        "completed": false,
        "created_at": "2026-02-09T10:00:00Z",
        "updated_at": "2026-02-09T10:00:00Z"
      }
    ]
  }
  ```
- **Failure (401)**:
  ```json
  {
    "error": "Unauthorized - invalid or missing token"
  }
  ```
- **Failure (403)**:
  ```json
  {
    "error": "Forbidden - user ID mismatch"
  }
  ```

---

## POST /api/users/{user_id}/tasks
**Purpose**: Create a new task for the authenticated user

### Request
- **Method**: POST
- **Path**: `/api/users/{user_id}/tasks`
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
  - Title must be provided

### Response
- **Success (201)**:
  ```json
  {
    "task": {
      "id": "task-uuid-string",
      "title": "New task",
      "description": "Task description",
      "completed": false,
      "created_at": "2026-02-09T10:00:00Z",
      "updated_at": "2026-02-09T10:00:00Z",
      "user_id": "user-uuid-string"
    }
  }
  ```
- **Failure (401)**:
  ```json
  {
    "error": "Unauthorized - invalid or missing token"
  }
  ```
- **Failure (403)**:
  ```json
  {
    "error": "Forbidden - user ID mismatch"
  }
  ```