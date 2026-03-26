from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.database import get_session
from src.services.auth_service import AuthService
from src.models.user import UserCreate, UserPublic
from src.auth.schemas import JWTResponse
from pydantic import BaseModel, EmailStr
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    """
    Schema for login request body
    """
    email: str
    password: str

@router.post("/register", response_model=UserPublic)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user
    """
    auth_service = AuthService(session)

    try:
        logger.info(f"Processing registration request for email: {user_create.email}")
        user = auth_service.register_user(user_create)
        logger.info(f"Successfully registered user with ID: {user.id}")
        return user
    except ValueError as e:
        logger.warning(f"Registration failed due to validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration"
        )

@router.post("/login", response_model=JWTResponse)
def login(login_data: LoginRequest, session: Session = Depends(get_session)):
    """
    Authenticate user and return access token
    """
    auth_service = AuthService(session)

    try:
        logger.info(f"Processing login request for email: {login_data.email}")
        user = auth_service.authenticate_user(login_data.email, login_data.password)

        if not user:
            logger.warning(f"Failed login attempt for email: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        token = auth_service.create_access_token_for_user(user)
        logger.info(f"Successful login for user ID: {user.id}")

        return JWTResponse(access_token=token)
    except HTTPException:
        # Re-raise HTTP exceptions as is
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login"
        )