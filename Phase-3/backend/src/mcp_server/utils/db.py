"""
Database Session Utility for MCP Tools.

Uses the same engine as the main app to avoid connection conflicts.
"""

from sqlmodel import Session
from src.database import engine

def get_session() -> Session:
    """Get a database session for MCP tools.
    
    Uses the main app's engine to ensure connection pooling consistency
    and avoid serverless connection issues.
    
    Usage:
        session = get_session()
        try:
            # Use session for database operations
            pass
        finally:
            session.close()
    """
    return Session(engine)
