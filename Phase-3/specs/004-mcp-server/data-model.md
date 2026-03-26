# Data Model: MCP Server & Task Tooling Layer

**Feature**: 004-mcp-server
**Date**: 2026-02-18
**Status**: Complete

## Existing Models (Reuse from Phase-2)

### Task Model

**Location**: `backend/src/models/task.py`

The MCP server reuses the existing Task model from Phase-2 without modifications.

```python
class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: str  # Foreign key to associate task with user
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Task(TaskBase, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
```

**Fields**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | str | Auto-generated | UUID primary key |
| title | str | Yes | Task title (1-200 chars) |
| description | str | No | Task description (max 1000 chars) |
| completed | bool | Default: false | Completion status |
| user_id | str | Yes | Owner user ID (foreign key) |
| created_at | datetime | Auto-generated | Creation timestamp |
| updated_at | datetime | Auto-generated | Last update timestamp |

**Validation Rules**:
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters
- `completed`: Boolean, defaults to false
- `user_id`: Required, must match authenticated user

**Relationships**:
- Many-to-one with User (via `user_id`)
- All queries scoped by `user_id` for isolation

## New Models (MCP-Specific)

### ToolExecutionLog Model

**Location**: `backend/src/models/mcp.py` (new file)

Optional audit model for tracking tool invocations (development/debugging only).

```python
class ToolExecutionLogBase(SQLModel):
    user_id: str
    tool_name: str
    invocation_inputs: dict  # JSONB field
    success: bool
    error_message: Optional[str] = None
    execution_time_ms: int
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class ToolExecutionLog(ToolExecutionLogBase, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
```

**Purpose**: Audit trail for hackathon reviewability
**Retention**: Development phase only (can be disabled in production)

## Database Queries (User Isolation Enforcement)

### List Tasks Query
```python
from sqlmodel import select

def list_tasks_for_user(session: Session, user_id: str) -> list[Task]:
    """Get all tasks for a specific user (enforces isolation)."""
    statement = select(Task).where(Task.user_id == user_id)
    results = session.exec(statement)
    return list(results.all())
```

### Create Task Query
```python
def create_task(session: Session, user_id: str, title: str, description: str = None) -> Task:
    """Create a new task owned by the specified user."""
    task = Task(
        title=title,
        description=description,
        user_id=user_id,
        completed=False
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Update Task Query (with Ownership Check)
```python
def update_task_if_owned(
    session: Session,
    user_id: str,
    task_id: str,
    updates: dict
) -> Task | None:
    """Update a task only if owned by the specified user."""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return None  # Ownership violation
    
    for field, value in updates.items():
        setattr(task, field, value)
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Delete Task Query (with Ownership Check)
```python
def delete_task_if_owned(
    session: Session,
    user_id: str,
    task_id: str
) -> bool:
    """Delete a task only if owned by the specified user. Returns True if deleted."""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return False  # Ownership violation
    
    session.delete(task)
    session.commit()
    return True
```

## Schema Evolution

### Migration Strategy
- No changes to existing Task model (backward compatible)
- Optional `ToolExecutionLog` table created via new migration
- Migration script location: `backend/migrations/004_add_mcp_tool_logs.sql`

### Migration Script
```sql
-- Migration 004: Add MCP tool execution logs (optional)
CREATE TABLE IF NOT EXISTS tool_execution_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    invocation_inputs JSONB NOT NULL,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    execution_time_ms INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for user-scoped queries
CREATE INDEX idx_tool_logs_user_id ON tool_execution_logs(user_id);
```

## Data Validation at Database Level

### Constraints
- `NOT NULL` on required fields (title, user_id)
- `DEFAULT FALSE` on completed field
- UUID format on primary keys
- Foreign key relationship to users table (if exists)

### Indexes
- Primary key index on `task.id` (auto-created)
- Foreign key index on `task.user_id` (for fast user-scoped queries)
- Composite index on `(user_id, created_at)` for sorted list queries
