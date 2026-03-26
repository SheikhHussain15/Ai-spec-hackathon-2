from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash a plain password
    """
    # Check password length before hashing to avoid bcrypt limitations
    # bcrypt has a 72-byte limit, but we need to account for UTF-8 encoding
    password_bytes = password.encode('utf-8')
    print(f"Password: {password}")
    print(f"Password length in bytes: {len(password_bytes)}")
    
    if len(password_bytes) > 72:
        # Truncate to 72 bytes and decode back to string
        # Note: This could potentially alter multi-byte characters
        truncated_password = password_bytes[:72].decode('utf-8', errors='ignore')
        print(f"Truncating password to: {truncated_password}")
        return pwd_context.hash(truncated_password)
    
    try:
        result = pwd_context.hash(password)
        print(f"Hash successful: {result[:20]}...")
        return result
    except Exception as e:
        # Log the actual error for debugging
        print(f"Bcrypt error: {e}")
        # Re-raise with a more specific message
        raise ValueError(f"Password hashing failed: {str(e)}")

# Test with various passwords
test_passwords = [
    "short",
    "testpass",
    "securepassword123",
    "verylongpasswordthatmightexceedthebcryptlimitforatext"
]

for pwd in test_passwords:
    print(f"\n--- Testing password: '{pwd}' ---")
    try:
        hash_result = get_password_hash(pwd)
        print(f"Success: {hash_result[:30]}...")
    except Exception as e:
        print(f"Error: {e}")