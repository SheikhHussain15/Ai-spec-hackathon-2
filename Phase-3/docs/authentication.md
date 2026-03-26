# Authentication & Security Foundation Documentation

## Overview
This document describes the authentication and security foundation for the multi-user todo web application. The system implements JWT-based authentication with strict user data isolation.

## Architecture
- **Frontend**: Next.js 16+ with App Router
- **Backend**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (JWT-based)

## Authentication Flow
1. User registers/login via frontend
2. Better Auth issues JWT with user_id and email claims
3. Frontend stores JWT and attaches to all API requests
4. Backend verifies JWT signature and expiry
5. Backend enforces user ID matching between token and URL path
6. Access granted or denied based on validation

## Security Features
- Stateless authentication (no server-side sessions)
- JWT-based with configurable expiry
- User data isolation enforcement
- Protection against cross-user access
- Secure password hashing
- Proper error handling for auth failures

## API Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/users/{user_id}/tasks` - Get user's tasks
- `POST /api/users/{user_id}/tasks` - Create user's task
- `GET /api/users/{user_id}` - Get user info

## Error Handling
- 401 Unauthorized: Invalid, missing, or expired tokens
- 403 Forbidden: User ID mismatch between token and URL
- 404 Not Found: Resource doesn't exist
- 422 Unprocessable Entity: Invalid request format