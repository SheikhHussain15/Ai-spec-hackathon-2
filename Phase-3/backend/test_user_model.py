import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from src.models.user import UserCreate

# Test creating a UserCreate object with a valid password
try:
    user_data = UserCreate(
        email="test@example.com",
        password="TempPass"
    )
    print("UserCreate object created successfully")
    print(f"Email: {user_data.email}")
    print(f"Password: {user_data.password}")
except Exception as e:
    print(f"Error creating UserCreate object: {e}")
    import traceback
    traceback.print_exc()