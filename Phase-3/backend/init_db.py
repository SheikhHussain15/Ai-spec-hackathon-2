"""
Initialize Database Tables

Creates all tables in the Neon PostgreSQL database
"""

from src.database import engine
from sqlmodel import SQLModel
from src.models.user import User
from src.models.task import Task
from src.models.conversation import Conversation, Message

print("Initializing database tables...")
print("Database URL:", engine.url)
print()

# Create all tables
try:
    SQLModel.metadata.create_all(bind=engine)
    print("[OK] Database tables created successfully!")
    print()
    print("Tables created:")
    print("  - user")
    print("  - task")  
    print("  - conversations")
    print("  - messages")
except Exception as e:
    print(f"[ERROR] Failed to create tables: {e}")
    print()
    print("Please check your DATABASE_URL in .env file")
