# Backend API & Data Layer Documentation

## Overview
This document describes the backend API and data layer for the multi-user todo web application. The system implements secure, RESTful task management with persistent storage in Neon Serverless PostgreSQL and strict user-scoped data access.

## API Endpoints

### Authentication Required
All endpoints require a valid JWT in the Authorization header: `Authorization: Bearer <JWT_TOKEN>`

### Task Management Endpoints

#### GET `/api/tasks/{user_id}/tasks`
Retrieve all tasks for the specified user.

**Path Parameters:**
- `user_id` (string): The ID of the user whose tasks to retrieve. Must match the user_id in the JWT token.

**Response:**
- `200 OK`: Array of Task objects
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: user_id in path doesn't match token

**Example Response:**
```json
[
  {
    "id": "task-uuid-string",
    "title": "Sample task",
    "description": "Task description",
    "completed": false,
    "user_id": "user-uuid-string",
    "created_at": "2026-02-09T10:00:00",
    "updated_at": "2026-02-09T10:00:00"
  }
]
```

#### POST `/api/tasks/{user_id}/tasks`
Create a new task for the specified user.

**Path Parameters:**
- `user_id` (string): The ID of the user creating the task. Must match the user_id in the JWT token.

**Request Body:**
```json
{
  "title": "New task title",
  "description": "Task description",
  "completed": false
}
```

**Response:**
- `201 Created`: The created Task object
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: user_id in path doesn't match token

#### GET `/api/tasks/{user_id}/tasks/{task_id}`
Retrieve a specific task for the specified user.

**Path Parameters:**
- `user_id` (string): The ID of the user whose task to retrieve. Must match the user_id in the JWT token.
- `task_id` (string): The ID of the task to retrieve.

**Response:**
- `200 OK`: The Task object
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: user_id in path doesn't match token
- `404 Not Found`: Task not found

#### PUT `/api/tasks/{user_id}/tasks/{task_id}`
Update a specific task for the specified user.

**Path Parameters:**
- `user_id` (string): The ID of the user whose task to update. Must match the user_id in the JWT token.
- `task_id` (string): The ID of the task to update.

**Request Body:**
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

**Response:**
- `200 OK`: The updated Task object
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: user_id in path doesn't match token
- `404 Not Found`: Task not found

#### PATCH `/api/tasks/{user_id}/tasks/{task_id}/complete`
Update only the completion status of a specific task for the specified user.

**Path Parameters:**
- `user_id` (string): The ID of the user whose task to update. Must match the user_id in the JWT token.
- `task_id` (string): The ID of the task to update.

**Request Body:**
```json
{
  "completed": true
}
```

**Response:**
- `200 OK`: The updated Task object
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: user_id in path doesn't match token
- `404 Not Found`: Task not found

#### DELETE `/api/tasks/{user_id}/tasks/{task_id}`
Delete a specific task for the specified user.

**Path Parameters:**
- `user_id` (string): The ID of the user whose task to delete. Must match the user_id in the JWT token.
- `task_id` (string): The ID of the task to delete.

**Response:**
- `204 No Content`: Task successfully deleted
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: user_id in path doesn't match token
- `404 Not Found`: Task not found

## Data Models

### Task
Represents a user's task with the following properties:

- `id` (string): Unique identifier for the task
- `title` (string): Title of the task (required)
- `description` (string, optional): Description of the task
- `completed` (boolean): Completion status of the task (default: false)
- `user_id` (string): ID of the user who owns the task
- `created_at` (datetime): Timestamp when the task was created
- `updated_at` (datetime): Timestamp when the task was last updated

## Security Features

### User Data Isolation
- All database queries are filtered by the authenticated user's ID
- Users cannot access, modify, or delete tasks belonging to other users
- The user_id in the URL path is validated against the user_id in the JWT token

### Authentication
- All endpoints require a valid JWT in the Authorization header
- Tokens are validated for signature, expiration, and claims
- Invalid, missing, or expired tokens return HTTP 401

## Database Schema

The application uses SQLModel for database operations with the following table:

### tasks table
- `id` (VARCHAR, PRIMARY KEY): Unique identifier for the task
- `title` (VARCHAR, NOT NULL): Title of the task
- `description` (VARCHAR, NULLABLE): Description of the task
- `completed` (BOOLEAN, DEFAULT false): Completion status of the task
- `user_id` (VARCHAR, NOT NULL): ID of the user who owns the task
- `created_at` (TIMESTAMP, NOT NULL): Timestamp when the task was created
- `updated_at` (TIMESTAMP, NOT NULL): Timestamp when the task was last updated

## Error Handling

- `401 Unauthorized`: Returned when the request lacks valid authentication credentials
- `403 Forbidden`: Returned when a user attempts to access resources they don't own
- `404 Not Found`: Returned when the requested resource doesn't exist
- `422 Unprocessable Entity`: Returned when the request contains invalid data