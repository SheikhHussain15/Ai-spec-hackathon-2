from fastapi import Request, HTTPException, status
from src.auth.schemas import TokenData

def validate_user_id_from_path(
    request: Request,
    current_user: TokenData
) -> bool:
    """
    Validates that the user_id in the URL path matches the user_id in the JWT token
    """
    # Extract user_id from the path parameters
    path_user_id = request.path_params.get('user_id')
    
    if not path_user_id:
        # If there's no user_id in the path, we can't validate
        # This might be a case where the endpoint doesn't require user-specific access
        return True
    
    # Compare the user_id in the path with the user_id in the token
    if path_user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: Path user_id '{path_user_id}' does not match token user_id '{current_user.user_id}'"
        )
    
    return True