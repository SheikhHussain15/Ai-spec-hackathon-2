from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: str  # Foreign key to associate task with user
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Task(TaskBase, table=True):
    """
    Task model representing a task in the system
    """
    id: str = Field(default_factory=generate_uuid, primary_key=True)

class TaskPublic(TaskBase):
    """
    Public representation of a task (without sensitive data)
    """
    id: str
    created_at: datetime
    updated_at: datetime

class TaskCreateRequest(SQLModel):
    """
    Schema for creating a new task (request body)
    """
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    """
    Schema for creating a new task (internal use)
    """
    title: str

class TaskUpdate(SQLModel):
    """
    Schema for updating a task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskPatchComplete(SQLModel):
    """
    Schema for updating only the completion status of a task
    """
    completed: bool