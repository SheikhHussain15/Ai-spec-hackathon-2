---
id: 014
title: Fix Auth Registration and Login Errors
stage: green
date: 2026-02-17
surface: agent
model: Qwen
feature: authentication
branch: auth-bug-fix
user: user
command: /debug
labels: ["bugfix", "authentication", "login", "signup", "green-stage"]
links:
  spec: null
  plan: null
  tasks: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/src/models/user.py
 - backend/src/services/auth_service.py
 - backend/.env
 - frontend/.env.local
 - backend/test_auth_auto.py
tests:
 - backend/test_auth_endpoints.py
 - backend/test_auth_auto.py
---

## Prompt

User's original issue: "registration failed or login failed error"

## Response snapshot

Successfully debugged and fixed authentication registration and login failures. The following issues were identified and resolved:

### Root Causes Found:

1. **Missing `name` field in UserCreate model**: The frontend was sending a `name` field during registration, but the Pydantic models in `backend/src/models/user.py` did not include this field, causing validation failures.

2. **Missing environment configuration files**: The backend lacked proper `.env` configuration for JWT settings and database URL, and the frontend was missing the API URL configuration.

3. **Incorrect API URL configuration in frontend**: The frontend `.env.local` had `NEXT_PUBLIC_API_URL=http://localhost:8000/api`, but the axios client already adds the `/api` prefix, resulting in double prefixing (`/api/api/...`).

### Fixes Applied:

**1. Fixed User Model (`backend/src/models/user.py`):**
- Added `name: str` field to `UserBase` model
- This propagates to `User`, `UserPublic`, and `UserCreate` models
- Ensures frontend registration data is properly validated

**2. Created Environment Files:**
- `backend/.env`:
  ```
  JWT_SECRET=your-secret-key-here
  JWT_ALGORITHM=HS256
  JWT_EXPIRATION_HOURS=24
  DATABASE_URL=sqlite+aiosqlite:///./todo_app.db
  ```
- `frontend/.env.local`:
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```

**3. Fixed auth_service.py:**
- Updated user registration to properly save the `name` field to the database
- Ensures user data is persisted correctly during signup

**4. Fixed Frontend API URL:**
- Changed from `http://localhost:8000/api` to `http://localhost:8000`
- Prevents double `/api` prefix issue

**5. Created Test Scripts:**
- `backend/test_auth_endpoints.py`: Manual verification of auth endpoints
- `backend/test_auth_auto.py`: Automated testing of signup and login flows

### Tests Passed:
- ✅ Backend signup endpoint: PASS (returns user data with id, email, name)
- ✅ Backend login endpoint: PASS (returns JWT token)

## Outcome

- ✅ Impact: Authentication registration and login now working correctly
- 🧪 Tests: 2 test scripts created for endpoint verification
- 📁 Files: 5 files modified/created (2 models/services, 2 env files, 1 test script)
- 🔁 Next prompts: Ready for frontend integration testing
- 🧠 Reflection: Root causes were model mismatch, missing config, and URL misconfiguration

## Evaluation notes (flywheel)

- Failure modes observed: 
  1. Pydantic validation error due to missing `name` field
  2. Missing environment variables causing runtime errors
  3. Double `/api` prefix causing 404 errors
- Graders run and results (PASS/FAIL): PASS - Both signup and login endpoints verified
- Prompt variant (if applicable): Debug session for authentication bug fix
- Next experiment: Full end-to-end testing with frontend UI
