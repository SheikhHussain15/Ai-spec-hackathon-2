"""
Database Setup Script

Creates all database tables if they don't exist
"""

from src.database import engine
from sqlmodel import SQLModel
from src.models.user import User
from src.models.task import Task
from src.models.conversation import Conversation, Message

def setup_database():
    """Create all database tables"""
    print("Creating database tables...")
    
    # Create all tables
    SQLModel.metadata.create_all(bind=engine)
    
    print("✓ All tables created successfully!")
    print("\nTables created:")
    print("  - user")
    print("  - task")
    print("  - conversations")
    print("  - messages")

if __name__ == "__main__":
    setup_database()
