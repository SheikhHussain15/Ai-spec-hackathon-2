from pydantic import BaseModel
from typing import Optional

class JWTPayload(BaseModel):
    """
    Schema for JWT payload claims
    """
    user_id: str
    email: str
    exp: int  # Expiration time (as Unix timestamp)
    iat: int  # Issued at time (as Unix timestamp)
    sub: Optional[str] = None  # Subject (optional, but recommended)

class JWTResponse(BaseModel):
    """
    Schema for JWT response when issuing tokens
    """
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """
    Schema for extracted token data
    """
    user_id: str
    email: str