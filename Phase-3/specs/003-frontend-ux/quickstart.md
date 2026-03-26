# Quickstart Guide: Frontend Application & UX

## Overview
This guide explains how to set up and run the frontend application for the Multi-User Todo Web Application.

## Prerequisites
- Node.js 18+ 
- npm or yarn
- Access to the backend API (running on http://localhost:8000 by default)

## Setup Instructions

### 1. Environment Variables
Set up the following environment variables in a `.env.local` file:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
```

### 2. Install Dependencies
```bash
cd frontend
npm install
```

### 3. Run the Application
```bash
# Development mode
npm run dev

# Production build
npm run build
npm start
```

The application will be available at `http://localhost:3000`.

## Frontend Structure
The frontend follows the Next.js App Router structure:

```
frontend/
├── src/
│   ├── app/                 # Next.js 16+ App Router structure
│   │   ├── (auth)/          # Public routes (login, signup)
│   │   │   ├── login/
│   │   │   └── signup/
│   │   ├── tasks/           # Protected route for task management
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Home page
│   ├── components/          # Reusable UI components
│   │   ├── auth/
│   │   ├── tasks/
│   │   ├── ui/              # Base UI components
│   │   └── common/          # Shared components
│   ├── services/            # API services and authentication
│   │   ├── auth/
│   │   ├── api-client/
│   │   └── middleware/
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utility functions
│   ├── styles/              # Global styles and Tailwind config
│   └── types/               # TypeScript type definitions
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

## Key Features

### Authentication Flow
1. Users can navigate to `/signup` to create an account
2. Users can navigate to `/login` to sign in
3. JWT tokens are automatically stored and attached to API requests
4. Unauthenticated users are redirected to login when accessing protected routes

### Task Management
1. Authenticated users can access `/tasks` to view their tasks
2. Users can create new tasks with title and description
3. Users can mark tasks as complete/incomplete
4. Users can edit or delete their tasks

### Route Protection
- Public routes: `/login`, `/signup`
- Protected routes: `/tasks` and any subroutes
- Route guard redirects unauthenticated users to login page

## API Integration
The frontend communicates with the backend API using a centralized API client that:
- Attaches JWT tokens to all requests automatically
- Handles loading, error, and success states
- Provides consistent error messaging
- Implements proper error handling for 401 responses

## Testing
Run the tests using the appropriate command:

```bash
# Unit tests
npm run test:unit

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e
```

## Validation Steps
1. Verify that signup/login works correctly
2. Confirm that unauthenticated users cannot access protected routes
3. Test task creation, viewing, updating, and deletion
4. Verify that JWT tokens are properly attached to API requests
5. Test error handling for invalid inputs and API failures
6. Confirm responsive design works on different screen sizes