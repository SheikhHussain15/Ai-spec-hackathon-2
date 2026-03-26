# Data Model: Frontend Application & UX

## User Entity (Frontend Representation)
- **Fields**:
  - id (string): Unique identifier for the user
  - email (string): User's email address
  - isLoggedIn (boolean): Current authentication status
  - session (object): Session information including JWT token
- **Validation rules**:
  - Email must be valid format
  - Session must contain valid JWT token
  - User data must be refreshed periodically to ensure validity

## Task Entity (Frontend Representation)
- **Fields**:
  - id (string): Unique identifier for the task
  - title (string): Title of the task (required)
  - description (string, optional): Description of the task
  - completed (boolean): Completion status of the task (default: false)
  - user_id (string): ID of the user who owns the task
  - created_at (string): Timestamp when the task was created (ISO format)
  - updated_at (string): Timestamp when the task was last updated (ISO format)
- **Validation rules**:
  - Title must be provided and not empty
  - Title must not exceed 255 characters
  - Description must not exceed 1000 characters
  - user_id must match the authenticated user
  - created_at and updated_at are read-only from API

## UI State Entity
- **Fields**:
  - isLoading (boolean): Indicates if data is being loaded
  - isError (boolean): Indicates if an error occurred
  - isEmpty (boolean): Indicates if there's no data to display
  - errorMessage (string, optional): Error message to display
  - successMessage (string, optional): Success message to display
- **Validation rules**:
  - Only one of isLoading, isError, or isEmpty should be true at a time
  - Error messages should be cleared after a certain time period
  - Success messages should be cleared after a certain time period

## API Request Structure
- **Headers**:
  - Authorization (string): Format "Bearer <JWT_TOKEN>"
  - Content-Type (string): Format "application/json" for POST/PUT requests
- **Validation rules**:
  - Authorization header must be present for all protected API requests
  - Request body must conform to appropriate schema (TaskCreate, TaskUpdate, etc.)
  - Response must be validated before updating UI state

## Route Protection Entity
- **Fields**:
  - path (string): The route path to protect
  - requiresAuth (boolean): Whether authentication is required
  - allowedRoles (array): Roles allowed to access the route (not used in this implementation)
- **Validation rules**:
  - Unauthenticated users must be redirected to login page
  - Session must be validated before granting access to protected routes
  - Redirect URL should be preserved for post-login navigation