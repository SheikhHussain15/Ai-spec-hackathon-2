from sqlmodel import Session, select
from passlib.context import CryptContext
from src.models.user import User, UserCreate, UserPublic
from src.auth.jwt_utils import create_access_token
from typing import Optional
from datetime import timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a plain password
    """
    # Check password length before hashing to avoid bcrypt limitations
    # bcrypt has a 72-byte limit, but we need to account for UTF-8 encoding
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes and decode back to string
        # Note: This could potentially alter multi-byte characters
        truncated_password = password_bytes[:72].decode('utf-8', errors='ignore')
        return pwd_context.hash(truncated_password)
    
    try:
        return pwd_context.hash(password)
    except Exception as e:
        # Log the actual error for debugging
        print(f"Bcrypt error: {e}")
        # Re-raise with a more specific message
        raise ValueError(f"Password hashing failed: {str(e)}")

class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def register_user(self, user_create: UserCreate) -> UserPublic:
        """
        Register a new user with the provided credentials
        """
        try:
            # Check if user already exists
            existing_user = self.session.exec(
                select(User).where(User.email == user_create.email)
            ).first()

            if existing_user:
                logger.warning(f"Registration attempt with already registered email: {user_create.email}")
                raise ValueError("Email already registered")

            # Hash the password
            hashed_password = get_password_hash(user_create.password)

            # Create the user
            db_user = User(
                email=user_create.email,
                name=user_create.name,
                hashed_password=hashed_password
            )

            self.session.add(db_user)
            self.session.commit()
            self.session.refresh(db_user)

            logger.info(f"Successfully registered new user with email: {user_create.email}")

            # Return public representation
            return UserPublic.model_validate(db_user)
        except ValueError:
            # Re-raise ValueError as is since it's a business logic error
            raise
        except Exception as e:
            logger.error(f"Unexpected error during user registration: {str(e)}")
            raise ValueError(f"Registration failed due to server error: {str(e)}")

    def authenticate_user(self, email: str, password: str) -> Optional[UserPublic]:
        """
        Authenticate a user with email and password
        """
        # Find user by email
        user = self.session.exec(
            select(User).where(User.email == email)
        ).first()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        # Return public representation
        return UserPublic.model_validate(user)

    def create_access_token_for_user(self, user: UserPublic) -> str:
        """
        Create an access token for the given user
        """
        data = {
            "user_id": user.id,
            "email": user.email
        }
        
        # Set token to expire in 30 minutes
        expire = timedelta(minutes=30)
        token = create_access_token(data=data, expires_delta=expire)
        
        return token