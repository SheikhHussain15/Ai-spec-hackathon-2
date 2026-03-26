from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

app = FastAPI()

# Simple models for testing
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

# In-memory "database" for testing
users_db = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.post("/api/auth/register", response_model=User)
def register_user(user_data: UserCreate):
    # Check if user already exists
    for user in users_db:
        if user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Create new user
    new_user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    users_db.append(new_user)
    return new_user

@app.get("/health")
def health_check():
    return {"status": "healthy"}