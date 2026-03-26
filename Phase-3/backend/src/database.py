from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback to SQLite if no DATABASE_URL is set
    DATABASE_URL = "sqlite:///./todo_app.db"
    print(f"Warning: DATABASE_URL not set, using SQLite: {DATABASE_URL}")
else:
    print(f"Using database: {DATABASE_URL[:50]}...")

# Create the database engine with serverless-friendly settings
connect_args = {}
if DATABASE_URL.startswith("postgresql"):
    # For PostgreSQL, use settings that work well with serverless
    connect_args = {
        "pool_pre_ping": True,  # Verify connections before use
        "pool_recycle": 300,    # Recycle connections every 5 minutes
    }

engine = create_engine(
    DATABASE_URL,
    echo=False,  # Disable SQL logging by default
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    **connect_args
)

def get_session():
    with Session(engine) as session:
        yield session