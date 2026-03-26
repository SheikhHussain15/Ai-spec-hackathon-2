from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class User(UserBase, table=True):
    """
    User model representing a registered user in the system
    """
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    hashed_password: str

class UserPublic(UserBase):
    """
    Public representation of a user (without sensitive data)
    """
    id: str
    name: Optional[str]
    created_at: datetime
    updated_at: datetime

class UserCreate(UserBase):
    """
    Schema for creating a new user
    """
    password: str = Field(min_length=8, max_length=72)

class UserUpdate(SQLModel):
    """
    Schema for updating a user
    """
    email: Optional[str] = None
    password: Optional[str] = None