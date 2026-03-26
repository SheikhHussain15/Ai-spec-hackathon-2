"""
Conversation Service for AI chat orchestration.

Handles conversation lifecycle: get/create conversations, store messages, retrieve history.
"""

from sqlmodel import Session, select
from datetime import datetime
from typing import List, Optional

from src.models.conversation import (
    Conversation,
    ConversationCreate,
    Message,
    MessageCreate,
    MessagePublic,
)
from src.agent.config import conversation_config


def get_or_create_conversation(
    session: Session,
    user_id: str,
    conversation_id: Optional[str] = None
) -> Conversation:
    """
    Get existing conversation or create new one.
    
    Args:
        session: Database session
        user_id: Authenticated user ID
        conversation_id: Optional existing conversation ID
        
    Returns:
        Conversation instance (existing or newly created)
    """
    if conversation_id:
        # Try to get existing conversation
        conversation = session.get(Conversation, conversation_id)
        # Verify ownership
        if conversation and conversation.user_id == user_id:
            return conversation
    
    # Create new conversation
    conversation_create = ConversationCreate(user_id=user_id)
    conversation = Conversation.model_validate(conversation_create)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def store_message(
    session: Session,
    conversation_id: str,
    user_id: str,
    role: str,
    content: str,
    tool_calls: Optional[dict] = None
) -> Message:
    """
    Store a message in the conversation.
    
    Args:
        session: Database session
        conversation_id: Parent conversation ID
        user_id: Message author user ID
        role: "user" or "assistant"
        content: Message content
        tool_calls: Optional tool invocation metadata
        
    Returns:
        Created Message instance
    """
    # Validate role
    if role not in ["user", "assistant"]:
        raise ValueError(f"Invalid role: {role}. Must be 'user' or 'assistant'")
    
    # Create message
    message_create = MessageCreate(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_calls=tool_calls
    )
    message = Message.model_validate(message_create)
    session.add(message)
    session.commit()
    session.refresh(message)
    
    # Update conversation timestamp
    conversation = session.get(Conversation, conversation_id)
    if conversation:
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
        
        # Auto-generate title from first user message
        if not conversation.title and role == "user":
            # Use first 50 chars of message as title
            conversation.title = content[:conversation_config.title_max_length]
            session.add(conversation)
            session.commit()
    
    return message


def get_conversation_history(
    session: Session,
    user_id: str,
    conversation_id: str,
    max_messages: Optional[int] = None
) -> List[Message]:
    """
    Fetch conversation history for agent context.
    
    Args:
        session: Database session
        user_id: Authenticated user ID
        conversation_id: Conversation to fetch history for
        max_messages: Maximum messages to return (default from config)
        
    Returns:
        List of Message instances ordered by created_at
    """
    if max_messages is None:
        max_messages = conversation_config.max_history_messages
    
    # Fetch messages with user isolation
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .where(Message.user_id == user_id)
        .order_by(Message.created_at.asc())
        .limit(max_messages)
    )
    messages = session.exec(statement).all()
    return list(messages)


def get_user_conversations(
    session: Session,
    user_id: str,
    limit: int = 20
) -> List[Conversation]:
    """
    Get all conversations for a user.
    
    Args:
        session: Database session
        user_id: Authenticated user ID
        limit: Maximum conversations to return
        
    Returns:
        List of Conversation instances ordered by updated_at
    """
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
    )
    conversations = session.exec(statement).all()
    return list(conversations)


def get_conversation_with_messages(
    session: Session,
    user_id: str,
    conversation_id: str
) -> tuple[Conversation, List[Message]]:
    """
    Get conversation with full message history.
    
    Args:
        session: Database session
        user_id: Authenticated user ID
        conversation_id: Conversation ID
        
    Returns:
        Tuple of (Conversation, List[Message])
    """
    conversation = session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user_id:
        return None, []
    
    messages = get_conversation_history(session, user_id, conversation_id, max_messages=None)
    return conversation, messages
