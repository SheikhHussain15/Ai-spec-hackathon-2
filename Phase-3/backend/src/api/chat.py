"""
Chat API Endpoint for AI agent orchestration.

Provides POST /api/{user_id}/chat for natural language task management.
"""

from fastapi import APIRouter, HTTPException, Header, Depends
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from src.database import get_session
from sqlmodel import Session
from src.services.conversation_service import (
    get_or_create_conversation,
    store_message,
    get_conversation_history,
    get_user_conversations,
    get_conversation_with_messages,
)
from src.services.agent_service import run_agent_with_tools
from src.auth.jwt_utils import verify_token, decode_jwt
from src.auth.schemas import JWTPayload

router = APIRouter(prefix="/api", tags=["AI Chat"])


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    success: bool = True
    response: str
    conversation_id: str
    tool_calls: List[Dict[str, Any]] = []


class ConversationListResponse(BaseModel):
    """Response model for conversations list."""
    success: bool = True
    conversations: List[Dict[str, Any]]


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    authorization: Optional[str] = Header(None),
    session: Session = Depends(get_session)
):
    """
    Chat with AI agent for task management.
    
    This endpoint:
    1. Gets or creates a conversation
    2. Stores the user message
    3. Fetches conversation history
    4. Runs the agent with MCP tools
    5. Stores the assistant response
    6. Returns response with tool call trace
    
    Args:
        user_id: User ID from path (validated against JWT)
        request: Chat request with message and optional conversation_id
        authorization: JWT token from Authorization header
        session: Database session
        
    Returns:
        ChatResponse with agent response, conversation_id, and tool_calls
    """
    # Validate JWT and extract user info
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        # Extract token from "Bearer <token>" format
        token = authorization.replace("Bearer ", "")
        payload = decode_jwt(token)
        jwt_user_id = payload.get("user_id") or payload.get("sub")
        
        # Validate user_id matches JWT
        if jwt_user_id and jwt_user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="User ID mismatch - cannot access another user's conversation"
            )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    
    try:
        # 1. Get or create conversation
        conversation = get_or_create_conversation(
            session,
            user_id,
            request.conversation_id
        )
        
        # 2. Store user message
        store_message(
            session,
            conversation.id,
            user_id,
            role="user",
            content=request.message
        )
        
        # 3. Fetch conversation history
        history = get_conversation_history(session, user_id, conversation.id)
        
        # Convert to OpenAI message format
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in history
        ]
        
        # 4. Run agent with MCP tools
        assistant_response, tool_calls = await run_agent_with_tools(messages, user_id)
        
        # 5. Store assistant response with tool calls
        store_message(
            session,
            conversation.id,
            user_id,
            role="assistant",
            content=assistant_response,
            tool_calls={"calls": tool_calls} if tool_calls else None
        )
        
        # 6. Return response
        return ChatResponse(
            success=True,
            response=assistant_response,
            conversation_id=conversation.id,
            tool_calls=tool_calls
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.get("/{user_id}/conversations", response_model=ConversationListResponse)
async def get_conversations(
    user_id: str,
    authorization: Optional[str] = Header(None),
    session: Session = Depends(get_session)
):
    """
    Get all conversations for the authenticated user.
    
    Args:
        user_id: User ID from path
        authorization: JWT token from Authorization header
        session: Database session
        
    Returns:
        List of conversations with metadata
    """
    # Validate JWT
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_jwt(token)
        jwt_user_id = payload.get("user_id") or payload.get("sub")
        
        if jwt_user_id and jwt_user_id != user_id:
            raise HTTPException(status_code=403, detail="User ID mismatch")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    
    try:
        conversations = get_user_conversations(session, user_id, limit=20)
        
        return ConversationListResponse(
            success=True,
            conversations=[
                {
                    "id": conv.id,
                    "title": conv.title or "New Conversation",
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat(),
                }
                for conv in conversations
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversations: {str(e)}")


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation_history_endpoint(
    user_id: str,
    conversation_id: str,
    authorization: Optional[str] = Header(None),
    session: Session = Depends(get_session)
):
    """
    Get full message history for a specific conversation.
    
    Args:
        user_id: User ID from path
        conversation_id: Conversation ID
        authorization: JWT token from Authorization header
        session: Database session
        
    Returns:
        Conversation with full message history
    """
    # Validate JWT
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_jwt(token)
        jwt_user_id = payload.get("user_id") or payload.get("sub")
        
        if jwt_user_id and jwt_user_id != user_id:
            raise HTTPException(status_code=403, detail="User ID mismatch")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    
    try:
        conversation, messages = get_conversation_with_messages(
            session,
            user_id,
            conversation_id
        )
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "success": True,
            "conversation": {
                "id": conversation.id,
                "title": conversation.title or "New Conversation",
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
            },
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "tool_calls": msg.tool_calls,
                    "created_at": msg.created_at.isoformat(),
                }
                for msg in messages
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversation: {str(e)}")
