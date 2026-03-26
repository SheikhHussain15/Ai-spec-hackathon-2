---
id: 001
title: Update Project Constitution
stage: constitution
date: 2026-02-09
surface: agent
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "security", "spec-driven"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
tests:
 - none
---

## Prompt

$ARGUMENTS

Project: Secure Multi-User Todo Full-Stack Web Application (Spec-Driven, Agentic Development)

Core principles:
- Security by default (no unauthenticated or cross-user access)
- Spec-driven development (spec → plan → tasks → implementation)
- Zero manual coding (all code generated via Qwen Code)
- Clear separation of concerns (auth, backend, frontend)
- Deterministic and reviewable outputs at every phase

Key standards:
- Every feature must be explicitly derived from a written spec
- All API behavior must be deterministic and documented
- Authentication must be stateless and cryptographically verifiable
- User data isolation must be enforced at every layer
- Frontend must never bypass backend authorization logic

Technology standards:
- Frontend: Next.js 16+ with App Router
- Backend: FastAPI (Python)
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- Spec system: Qwen Code + Spec-Kit Plus

Security standards:
- All API endpoints require a valid JWT
- JWTs must be verified using a shared secret (BETTER_AUTH_SECRET)
- User identity must be derived from JWT claims only
- URL user_id must match authenticated user identity
- Invalid, missing, or expired tokens must return 401 Unauthorized
- No hardcoded secrets or credentials in source code

API standards:
- RESTful endpoint design
- Proper HTTP status codes for all operations
- Task ownership enforced on every query
- No cross-user reads or writes under any condition
- Backend must be stateless and session-free

Frontend standards:
- Auth-aware routing (public vs protected routes)
- JWT attached automatically to all API requests
- Clear UX feedback for loading, errors, and auth failures
- Responsive and accessible UI

Operational constraints:
- Serverless-compatible architecture
- Environment-based configuration (dev / prod)
- No background jobs, cron tasks, or websockets
- No role-based access control beyond single-user ownership

Evaluation constraints:
- All 5 basic-level Todo features implemented
- All required API endpoints implemented and secured
- Persistent storage via Neon PostgreSQL
- Authentication fully integrated end-to-end
- Entire development follows Agentic Dev Stack workflow

Success criteria:
- Every phase (spec, plan, tasks, implementation) is reviewable
- No unauthorized access paths exist
- Each user only sees and modifies their own tasks
- Application runs successfully as a multi-user web app
- Hackathon reviewers can trace implementation directly back to specs

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) with the specific principles and requirements for the Secure Multi-User Todo Full-Stack Web Application. Also updated the template files to align with the new constitution:

1. Updated .specify/memory/constitution.md with:
   - Security by Default principle
   - Spec-Driven Development principle
   - Zero Manual Coding principle
   - Technology Standardization principle
   - Security Enforcement principle
   - API Design Standards principle
   - Additional constraints and development workflow sections

2. Updated .specify/templates/plan-template.md to include a comprehensive Constitution Check section with compliance requirements for all principles.

3. Updated .specify/templates/spec-template.md to include security-focused functional requirements (FR-001 through FR-010).

4. Updated .specify/templates/tasks-template.md to include foundational security tasks in Phase 2 (T004 through T012).

## Outcome

- ✅ Impact: Project constitution and related templates updated with security-first, spec-driven principles
- 🧪 Tests: No automated tests for documentation changes
- 📁 Files: 4 files updated to align with new constitution
- 🔁 Next prompts: Proceed with feature specification based on updated constitution
- 🧠 Reflection: The constitution now properly reflects the security and technology requirements for the multi-user web application

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A for documentation changes
- Prompt variant (if applicable): N/A
- Next experiment: Begin feature specification using the updated constitution