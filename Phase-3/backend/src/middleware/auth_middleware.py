from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from src.auth.jwt_utils import verify_token
from src.auth.schemas import TokenData

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get the current user from the JWT token in the request
    """
    token = credentials.credentials
    
    token_data = verify_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token_data

def require_user_id_match(request: Request, current_user: TokenData = Depends(get_current_user)) -> bool:
    """
    Verify that the user_id in the JWT matches the user_id in the request path
    """
    # Extract user_id from the path parameters
    path_user_id = request.path_params.get('user_id')
    
    if path_user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )
    
    return True