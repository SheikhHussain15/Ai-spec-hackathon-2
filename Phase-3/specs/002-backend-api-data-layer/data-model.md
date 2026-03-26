# Data Model: Backend API & Data Layer

## Task Entity
- **Fields**:
  - id (string/UUID): Unique identifier for the task (primary key)
  - title (string): Title of the task (required)
  - description (string, optional): Description of the task
  - completed (boolean): Completion status of the task (default: false)
  - user_id (string): ID of the user who owns the task (foreign key reference)
  - created_at (datetime): Timestamp when the task was created (auto-generated)
  - updated_at (datetime): Timestamp when the task was last updated (auto-generated)
- **Relationships**: 
  - Belongs to: User entity (many-to-one)
- **Validation rules**:
  - Title must be provided
  - Title must not exceed 255 characters
  - Description must not exceed 1000 characters
  - user_id must reference an existing user
  - created_at and updated_at are automatically managed

## Task Schemas
- **TaskCreate**:
  - title (string): Required title of the task
  - description (string, optional): Optional description of the task
  - completed (boolean, optional): Initial completion status (default: false)
  - user_id (string): ID of the user creating the task
- **TaskUpdate**:
  - title (string, optional): Updated title of the task
  - description (string, optional): Updated description of the task
  - completed (boolean, optional): Updated completion status
- **TaskPatchComplete**:
  - completed (boolean): Updated completion status only
- **TaskPublic**:
  - id (string): Unique identifier for the task
  - title (string): Title of the task
  - description (string, optional): Description of the task
  - completed (boolean): Completion status of the task
  - user_id (string): ID of the user who owns the task
  - created_at (datetime): Timestamp when the task was created
  - updated_at (datetime): Timestamp when the task was last updated

## API Request Structure
- **Headers**:
  - Authorization (string): Format "Bearer <JWT_TOKEN>"
- **Path Parameters**:
  - user_id (string): The ID of the user making the request (must match JWT)
  - task_id (string): The ID of the specific task (when applicable)
- **Validation rules**:
  - Authorization header must be present for all task endpoints
  - user_id in path must match user_id in JWT token
  - task_id must reference an existing task owned by the user
  - Request body must conform to appropriate schema (TaskCreate, TaskUpdate, etc.)