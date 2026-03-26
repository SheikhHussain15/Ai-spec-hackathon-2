"""
Conversation and Message models for AI chat orchestration.

These models enable persistent conversation history with full user isolation.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from sqlalchemy import Column, JSON


def generate_uuid():
    """Generate a new UUID string."""
    return str(uuid.uuid4())


class ConversationBase(SQLModel):
    """Base conversation model with common fields."""
    user_id: str = Field(..., index=True)  # User isolation
    title: Optional[str] = Field(None, max_length=200)  # Auto-generated from first message
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a chat session.
    
    Relationships:
        - Has many Messages
        - Belongs to User (via user_id)
    """
    __tablename__ = "conversations"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationPublic(ConversationBase):
    """Public representation of conversation (for API response)."""
    id: str
    message_count: Optional[int] = None


class MessageBase(SQLModel):
    """Base message model with common fields."""
    conversation_id: str = Field(..., foreign_key="conversations.id", index=True)
    user_id: str = Field(..., index=True)  # Denormalized for efficient scoping
    role: str = Field(..., max_length=20)  # "user" or "assistant"
    content: str = Field(..., max_length=10000)
    tool_calls: Optional[dict] = Field(None, sa_column=Column(JSON))  # Tool call metadata
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Message(MessageBase, table=True):
    """
    Message model representing a chat message.
    
    Relationships:
        - Belongs to Conversation
        - References User (via user_id)
    """
    __tablename__ = "messages"
    
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    conversation: Conversation = Relationship(back_populates="messages")


class MessagePublic(MessageBase):
    """Public representation of message (for API response)."""
    id: str


class ConversationCreate(SQLModel):
    """Schema for creating a new conversation."""
    user_id: str
    title: Optional[str] = None


class MessageCreate(SQLModel):
    """Schema for creating a new message."""
    conversation_id: str
    user_id: str
    role: str
    content: str
    tool_calls: Optional[dict] = None
