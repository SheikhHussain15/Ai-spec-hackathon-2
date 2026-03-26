import pytest
from datetime import timedelta
from src.auth.jwt_utils import create_access_token, verify_token
from src.auth.schemas import TokenData

def test_create_and_verify_token():
    """Test that we can create a token and verify it correctly"""
    # Data to encode in the token
    test_data = {
        "user_id": "test_user_123",
        "email": "test@example.com"
    }
    
    # Create a token
    token = create_access_token(test_data)
    
    # Verify the token
    token_data = verify_token(token)
    
    # Check that the token data matches what we put in
    assert token_data is not None
    assert token_data.user_id == "test_user_123"
    assert token_data.email == "test@example.com"

def test_token_expiry():
    """Test that expired tokens are properly rejected"""
    # Create a token that expires immediately
    test_data = {
        "user_id": "test_user_123",
        "email": "test@example.com"
    }
    
    token = create_access_token(test_data, expires_delta=timedelta(seconds=-1))
    
    # This should return None because the token is expired
    token_data = verify_token(token)
    assert token_data is None

def test_invalid_token():
    """Test that invalid tokens are properly rejected"""
    # Try to verify an invalid token
    token_data = verify_token("invalid.token.string")
    assert token_data is None