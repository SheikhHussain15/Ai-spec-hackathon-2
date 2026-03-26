# Quickstart Guide: Backend API & Data Layer

## Overview
This guide explains how to set up and test the backend API & data layer for the multi-user todo web application.

## Prerequisites
- Python 3.11+
- Poetry or pip
- Neon Serverless PostgreSQL account

## Setup Instructions

### 1. Environment Variables
Set up the following environment variables:

**Backend (.env)**:
```bash
BETTER_AUTH_SECRET=your_jwt_secret_key_here
DATABASE_URL=your_neon_postgres_connection_string
```

### 2. Install Dependencies
```bash
# Backend
cd backend
poetry install
# or if using pip
pip install -r requirements.txt
```

### 3. Run the Application
```bash
# Backend
cd backend
poetry run uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` and the interactive documentation at `http://localhost:8000/docs`.

## Testing the API

### 1. Authentication
First, you need to authenticate to get a JWT token:
1. Register a user via POST `/api/auth/register`
2. Login via POST `/api/auth/login` to get your JWT token

### 2. Task Operations
Once authenticated, you can perform task operations:

**Get all tasks for a user:**
```bash
curl -X GET \
  "http://localhost:8000/api/tasks/{user_id}/tasks" \
  -H "accept: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Create a new task:**
```bash
curl -X POST \
  "http://localhost:8000/api/tasks/{user_id}/tasks" \
  -H "accept: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"New Task","description":"Task description","completed":false}'
```

**Get a specific task:**
```bash
curl -X GET \
  "http://localhost:8000/api/tasks/{user_id}/tasks/{task_id}" \
  -H "accept: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Update a task:**
```bash
curl -X PUT \
  "http://localhost:8000/api/tasks/{user_id}/tasks/{task_id}" \
  -H "accept: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Task","description":"Updated description","completed":true}'
```

**Update task completion status:**
```bash
curl -X PATCH \
  "http://localhost:8000/api/tasks/{user_id}/tasks/{task_id}/complete" \
  -H "accept: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
```

**Delete a task:**
```bash
curl -X DELETE \
  "http://localhost:8000/api/tasks/{user_id}/tasks/{task_id}" \
  -H "accept: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Validation Steps
1. Verify that all endpoints return appropriate HTTP status codes
2. Confirm that user isolation works (users can't access other users' tasks)
3. Test that timestamps are properly managed
4. Validate that all required fields are enforced
5. Verify error handling for invalid requests