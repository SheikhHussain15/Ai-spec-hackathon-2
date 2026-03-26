# Research: AI Agent & Stateless Chat Orchestration

**Feature**: 005-ai-agent-chat
**Date**: 2026-02-18
**Status**: Complete

## OpenAI Agents SDK Integration

### Decision: Use Official OpenAI Agents SDK with MCP Tool Integration

The OpenAI Agents SDK provides the standard interface for AI agent orchestration with built-in tool calling support.

**Installation**:
```bash
pip install openai-agents
```

**Agent Initialization Pattern**:
```python
from openai import OpenAI
from openai.types.beta import AssistantToolChoice

client = OpenAI(api_key=API_KEY)

agent = client.beta.assistants.create(
    model="gpt-4-turbo-preview",
    instructions="You are a helpful task management assistant. Use the available tools to help users manage their tasks.",
    tools=[
        {"type": "function", "function": add_task_schema},
        {"type": "function", "function": list_tasks_schema},
        {"type": "function", "function": complete_task_schema},
        {"type": "function", "function": delete_task_schema},
        {"type": "function", "function": update_task_schema},
    ]
)
```

**Tool Call Execution Pattern**:
```python
# Create thread and message
thread = client.beta.threads.create()
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_message
)

# Run agent
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=agent.id
)

# Process tool calls
while run.status == "requires_action":
    if run.required_action.submit_tool_outputs:
        tool_outputs = process_tool_calls(run.required_action.submit_tool_outputs.tool_calls)
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
```

**Alternatives Considered**:
- LangChain Agents: Rejected - adds unnecessary abstraction layer, ties to specific framework
- Custom LLM orchestration: Rejected - reinvents wheel, less reliable than official SDK
- Direct API calls: Rejected - missing built-in tool calling features

## Conversation History Management

### Decision: Fetch Full History Per Request with Context Window Management

Stateless design requires fetching full conversation history from database on every request. Context window limits are managed by truncating oldest messages if needed.

**History Retrieval Pattern**:
```python
from sqlmodel import select

def get_conversation_history(session: Session, user_id: str, conversation_id: str, max_messages: int = 50):
    """Fetch conversation history for user, limited to max_messages."""
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .where(Message.user_id == user_id)
        .order_by(Message.created_at.asc())
        .limit(max_messages)
    )
    messages = session.exec(statement).all()
    
    # Convert to OpenAI message format
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]
```

**Context Window Strategy**:
- Default limit: 50 messages (fits within GPT-4 context window)
- If conversation exceeds limit: Keep oldest 5 messages + newest 45 messages
- Rationale: Preserves conversation context while respecting LLM limits

**Message Formatting**:
- User messages: `{"role": "user", "content": "..."}`
- Assistant messages: `{"role": "assistant", "content": "..."}`
- Tool results: Included in assistant message metadata

## Stateless Agent Orchestration

### Decision: Single Request-Response Cycle with Full State Persistence

Agent execution follows stateless pattern: fetch state → execute agent → persist state → return response. No in-memory state between requests.

**Request Cycle**:
```python
async def chat(user_id: str, message: str, conversation_id: str = None):
    # 1. Get or create conversation
    conversation = get_or_create_conversation(user_id, conversation_id)
    
    # 2. Store user message
    store_message(conversation.id, role="user", content=message)
    
    # 3. Fetch history
    history = get_conversation_history(session, user_id, conversation.id)
    
    # 4. Execute agent with tools
    response, tool_calls = execute_agent_with_tools(history)
    
    # 5. Store assistant response
    store_message(conversation.id, role="assistant", content=response, tool_calls=tool_calls)
    
    # 6. Return response
    return {
        "response": response,
        "conversation_id": conversation.id,
        "tool_calls": tool_calls
    }
```

**Tool Call Capture**:
- Capture tool name, arguments, and result for each invocation
- Store in Message model for transparency (User Story 3)
- Include in API response for client-side display

**Error Handling Pattern**:
```python
def execute_tool_safely(tool_name: str, arguments: dict, user_id: str):
    try:
        result = invoke_mcp_tool(tool_name, arguments, user_id)
        return {"success": True, "result": result}
    except NotFoundError:
        return {"success": False, "error": "Task not found", "error_code": "NOT_FOUND"}
    except OwnershipViolationError:
        return {"success": False, "error": "Access denied", "error_code": "OWNERSHIP_VIOLATION"}
    except Exception as e:
        return {"success": False, "error": str(e), "error_code": "TOOL_ERROR"}
```

## Database Schema Design

### Decision: Conversation and Message Models with User Scoping

New models follow existing Phase-2/Phase-3 patterns with user_id scoping for isolation.

**Conversation Model**:
```python
class ConversationBase(SQLModel):
    user_id: str  # Foreign key for user isolation
    title: Optional[str] = None  # Auto-generated from first message
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Conversation(ConversationBase, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    messages: List["Message"] = Relationship(back_populates="conversation")
```

**Message Model**:
```python
class MessageBase(SQLModel):
    conversation_id: str  # Foreign key to conversation
    user_id: str  # Denormalized for efficient scoping
    role: str  # "user" or "assistant"
    content: str
    tool_calls: Optional[dict] = Field(sa_column=Column(JSON))  # Tool call metadata
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Message(MessageBase, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    conversation: Conversation = Relationship(back_populates="messages")
```

**Indexing Strategy**:
- Primary key index on `conversation.id` (auto-created)
- Foreign key index on `conversation.user_id` (for user-scoped queries)
- Composite index on `message(conversation_id, created_at)` (for history retrieval)
- Index on `message.user_id` (for user isolation enforcement)

**Migration Approach**:
- Create new migration file: `backend/migrations/005_add_conversation_models.sql`
- Use Alembic or raw SQL for schema creation
- Include rollback script for development

## Summary of Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Agent SDK | OpenAI Agents SDK | Official support, built-in tool calling, future-proof |
| History Management | Full fetch per request | Stateless design, simple implementation |
| Context Window | 50 message limit | Fits GPT-4 context, preserves context |
| State Persistence | Database only | Serverless-compatible, zero in-memory state |
| Tool Error Handling | Graceful with error codes | User-friendly messages, traceability |
| Database Models | Conversation + Message | Standard pattern, user-scoped |

## Unresolved Questions

None - all technical decisions resolved with documented rationales.
