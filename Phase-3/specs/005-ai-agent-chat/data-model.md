# Data Model: AI Agent & Stateless Chat Orchestration

**Feature**: 005-ai-agent-chat
**Date**: 2026-02-18
**Status**: Complete

## New Models

### Conversation Model

**Location**: `backend/src/models/conversation.py`

Represents a chat session between a user and the AI agent.

```python
class ConversationBase(SQLModel):
    """Base conversation model with common fields."""
    user_id: str = Field(..., index=True)  # User isolation
    title: Optional[str] = Field(None, max_length=200)  # Auto-generated from first message
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a chat session.
    """
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    messages: List["Message"] = Relationship(back_populates="conversation")

class ConversationPublic(ConversationBase):
    """Public representation of conversation (without sensitive data)."""
    id: str
    message_count: Optional[int] = None  # Computed field for API response
```

**Fields**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | str | Auto-generated | UUID primary key |
| user_id | str | Yes | Owner user ID (foreign key) |
| title | str | No | Conversation title (auto-generated) |
| created_at | datetime | Auto-generated | Creation timestamp |
| updated_at | datetime | Auto-generated | Last update timestamp |

**Validation Rules**:
- `user_id`: Required, must match authenticated user
- `title`: Optional, max 200 characters
- Auto-generated title from first message if not provided

### Message Model

**Location**: `backend/src/models/conversation.py`

Represents individual chat messages within a conversation.

```python
class MessageBase(SQLModel):
    """Base message model with common fields."""
    conversation_id: str = Field(..., foreign_key="conversation.id", index=True)
    user_id: str = Field(..., index=True)  # Denormalized for efficient scoping
    role: str = Field(..., max_length=20)  # "user" or "assistant"
    content: str = Field(..., max_length=10000)
    tool_calls: Optional[dict] = Field(None, sa_column=Column(JSON))  # Tool call metadata
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Message(MessageBase, table=True):
    """
    Message model representing a chat message.
    """
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    conversation: Conversation = Relationship(back_populates="messages")

class MessagePublic(MessageBase):
    """Public representation of message (for API response)."""
    id: str
    tool_calls: Optional[dict]  # Include tool call trace for transparency
```

**Fields**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | str | Auto-generated | UUID primary key |
| conversation_id | str | Yes | Parent conversation ID |
| user_id | str | Yes | Message author user ID |
| role | str | Yes | "user" or "assistant" |
| content | str | Yes | Message content (max 10000 chars) |
| tool_calls | dict | No | Tool invocation metadata (JSON) |
| created_at | datetime | Auto-generated | Message timestamp |

**Validation Rules**:
- `conversation_id`: Required, must reference existing conversation
- `user_id`: Required, must match conversation owner
- `role`: Required, must be "user" or "assistant"
- `content`: Required, max 10000 characters
- `tool_calls`: Optional, JSON object with tool call details

**Tool Calls Schema** (for assistant messages):
```json
{
  "calls": [
    {
      "tool_name": "add_task",
      "arguments": {"title": "My Task", "description": "..."},
      "result": {"success": true, "data": {"id": "task-123"}},
      "execution_time_ms": 45
    }
  ]
}
```

## Relationships

```
Conversation (1) ----< Message (N)

Conversation:
  - user_id: references User.id
  - has many Messages

Message:
  - conversation_id: references Conversation.id
  - user_id: denormalized from Conversation.user_id
  - role: "user" or "assistant"
```

## Database Queries

### Get or Create Conversation

```python
def get_or_create_conversation(
    session: Session,
    user_id: str,
    conversation_id: Optional[str] = None
) -> Conversation:
    """Get existing conversation or create new one."""
    if conversation_id:
        conversation = session.get(Conversation, conversation_id)
        if conversation and conversation.user_id == user_id:
            return conversation
    
    # Create new conversation
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation
```

### Store Message

```python
def store_message(
    session: Session,
    conversation_id: str,
    user_id: str,
    role: str,
    content: str,
    tool_calls: Optional[dict] = None
) -> Message:
    """Store a message in the conversation."""
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_calls=tool_calls
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    
    # Update conversation timestamp
    conversation = session.get(Conversation, conversation_id)
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)
    session.commit()
    
    return message
```

### Fetch Conversation History

```python
def get_conversation_history(
    session: Session,
    user_id: str,
    conversation_id: str,
    max_messages: int = 50
) -> List[Message]:
    """Fetch conversation history for agent context."""
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .where(Message.user_id == user_id)
        .order_by(Message.created_at.asc())
        .limit(max_messages)
    )
    messages = session.exec(statement).all()
    return messages
```

### Get Conversations for User

```python
def get_user_conversations(
    session: Session,
    user_id: str,
    limit: int = 20
) -> List[Conversation]:
    """Get all conversations for a user."""
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
    )
    conversations = session.exec(statement).all()
    return conversations
```

## Indexes

```sql
-- Conversation indexes
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_user_updated ON conversations(user_id, updated_at DESC);

-- Message indexes
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_conv_created ON messages(conversation_id, created_at ASC);
```

## Migration Script

**Location**: `backend/migrations/005_add_conversation_models.sql`

```sql
-- Migration 005: Add Conversation and Message models
-- Created: 2026-02-18
-- Feature: 005-ai-agent-chat

-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    title TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for efficient queries
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_user_updated ON conversations(user_id, updated_at DESC);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_conv_created ON messages(conversation_id, created_at ASC);

-- Add constraint for user isolation (conversation owner must match message user_id)
ALTER TABLE messages 
ADD CONSTRAINT check_message_user 
CHECK (user_id = (SELECT user_id FROM conversations WHERE id = conversation_id));
```

## Schema Evolution

### Backward Compatibility
- No changes to existing Task model (reused from Phase-2)
- New Conversation and Message tables are additive
- Existing authentication and user isolation patterns preserved

### Future Enhancements
- Add `metadata` JSONB field to Conversation for custom attributes
- Add `parent_message_id` to Message for threaded conversations
- Add full-text search indexes on message content
