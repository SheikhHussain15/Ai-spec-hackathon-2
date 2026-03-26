# Quickstart Guide: Authentication & Security Foundation

## Overview
This guide explains how to set up and test the authentication and security foundation for the multi-user todo web application.

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Neon Serverless PostgreSQL account
- Better Auth configured with JWT support

## Setup Instructions

### 1. Environment Variables
Set up the following environment variables:

**Backend (.env)**:
```bash
BETTER_AUTH_SECRET=your_jwt_secret_key_here
DATABASE_URL=your_neon_postgres_connection_string
```

**Frontend (.env.local)**:
```bash
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 2. Install Dependencies
```bash
# Backend
cd backend
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] sqlmodel

# Frontend
cd frontend
npm install better-auth @better-auth/react
```

### 3. Run the Applications
```bash
# Backend
cd backend
uvicorn src.main:app --reload --port 8000

# Frontend
cd frontend
npm run dev
```

## Testing the Authentication Flow

### 1. User Registration
1. Navigate to the registration page
2. Submit valid email and password
3. Verify that you receive a JWT token and user object in response

### 2. User Login
1. Navigate to the login page
2. Submit valid credentials
3. Verify that you receive a JWT token and user object in response

### 3. Protected API Access
1. Use the received JWT token in the Authorization header
2. Make a request to a protected endpoint (e.g., `/api/users/{user_id}/tasks`)
3. Verify that the request succeeds with a 200 status
4. Try with an invalid/expired token and verify a 401 response

### 4. User Isolation Test
1. Log in as User A and note the user ID and JWT
2. Log in as User B and note the user ID and JWT
3. Try to access User A's data using User B's JWT but with User A's ID in the URL
4. Verify that this request is rejected with a 403 Forbidden response

## Security Validation
- All API endpoints require a valid JWT in the Authorization header
- JWTs are validated for signature, expiration, and claims
- User ID in the URL path is compared with the user ID in the JWT claims
- Invalid, missing, or expired tokens return HTTP 401
- Cross-user access attempts return HTTP 403
- Backend remains stateless with no session storage