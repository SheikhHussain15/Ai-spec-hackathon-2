from fastapi import HTTPException, status
from typing import Any
from src.models.user import User
from sqlmodel import Session, select
from src.auth.schemas import TokenData

def verify_user_ownership(
    db_session: Session,
    resource_owner_id: str,
    current_user: TokenData
) -> bool:
    """
    Verify that the current user owns the resource they're trying to access
    """
    if resource_owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You don't own this resource"
        )
    
    return True

def verify_user_exists(db_session: Session, user_id: str) -> User:
    """
    Verify that a user with the given ID exists
    """
    user = db_session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

def verify_user_access_to_resource(
    db_session: Session,
    resource_table: Any,
    resource_id: str,
    current_user: TokenData
) -> Any:
    """
    Generic function to verify user access to a specific resource
    """
    # This is a simplified version - in practice, you'd need to know the owner field name
    # For now, assuming the resource has an 'owner_id' or 'user_id' field
    resource = db_session.get(resource_table, resource_id)
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    # Assuming the resource has a user_id field that indicates ownership
    if hasattr(resource, 'user_id'):
        if resource.user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't own this resource"
            )
    elif hasattr(resource, 'owner_id'):
        if resource.owner_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't own this resource"
            )
    else:
        # If no ownership field exists, we can't verify ownership
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ownership verification not possible for this resource type"
        )
    
    return resource