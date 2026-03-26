from datetime import datetime, timedelta
from fastapi import HTTPException, status
from src.auth.jwt_utils import verify_token
from src.auth.schemas import TokenData

def validate_jwt_expiry(token: str) -> TokenData:
    """
    Validate that the JWT is not expired and return the token data
    """
    token_data = verify_token(token)
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid, expired, or malformed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token_data

def is_token_expired(token: str) -> bool:
    """
    Check if the token is expired without raising an exception
    """
    try:
        payload = verify_token(token)
        return payload is None
    except Exception:
        return True

def get_time_until_expiry(token: str) -> int:
    """
    Get the time in seconds until the token expires
    Returns negative value if already expired
    """
    try:
        from jose import jwt
        import os
        
        SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback-test-secret-key-change-in-production")
        ALGORITHM = "HS256"
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        
        if exp is None:
            return -1  # No expiration time in token
        
        current_time = int(datetime.utcnow().timestamp())
        return exp - current_time
    except Exception:
        return -1  # Error decoding token