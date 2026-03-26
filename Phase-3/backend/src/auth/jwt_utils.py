from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel

# Get the secret from environment variables
import os

# Use the JWT_SECRET from environment, falling back to BETTER_AUTH_SECRET for compatibility
SECRET_KEY = os.getenv("JWT_SECRET") or os.getenv("BETTER_AUTH_SECRET", "fallback-test-secret-key-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRATION_HOURS", 168)) * 60  # Convert hours to minutes

class TokenData(BaseModel):
    user_id: str
    email: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token with the provided data
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default expiration based on environment variable
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify the provided token and return the token data if valid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            return None

        user_id: str = payload.get("user_id")
        email: str = payload.get("email")

        if user_id is None or email is None:
            return None

        token_data = TokenData(user_id=user_id, email=email)
        return token_data
    except jwt.PyJWTError:
        return None
    except Exception:
        return None


def decode_jwt(token: str) -> dict:
    """
    Decode JWT token and return payload as dictionary.
    Does not verify expiration - use verify_token() for that.
    """
    try:
        # Decode without verification to get payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )