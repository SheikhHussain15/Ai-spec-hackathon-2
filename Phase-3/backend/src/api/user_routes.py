from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.database import get_session
from src.middleware.auth_middleware import get_current_user
from src.auth.schemas import TokenData
from src.models.user import User, UserPublic

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserPublic)
def get_user(
    user_id: str,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get user information.
    The user_id in the path must match the user_id in the JWT token.
    """
    # Verify that the user_id in the path matches the user_id in the token
    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )

    # Get the user from the database
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserPublic.model_validate(user)