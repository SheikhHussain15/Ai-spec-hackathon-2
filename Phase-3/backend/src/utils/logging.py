import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class SecurityEventType(Enum):
    AUTH_LOGIN_SUCCESS = "AUTH_LOGIN_SUCCESS"
    AUTH_LOGIN_FAILURE = "AUTH_LOGIN_FAILURE"
    AUTH_REGISTER_SUCCESS = "AUTH_REGISTER_SUCCESS"
    AUTH_REGISTER_FAILURE = "AUTH_REGISTER_FAILURE"
    AUTH_UNAUTHORIZED_ACCESS = "AUTH_UNAUTHORIZED_ACCESS"
    AUTH_INVALID_CREDENTIALS = "AUTH_INVALID_CREDENTIALS"
    DATA_ACCESS_ATTEMPT = "DATA_ACCESS_ATTEMPT"
    DATA_ACCESS_DENIED = "DATA_ACCESS_DENIED"

def log_security_event(
    event_type: SecurityEventType,
    user_id: str = None,
    ip_address: str = None,
    details: Dict[str, Any] = None
):
    """
    Log security-related events for monitoring and analysis
    """
    event_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type.value,
        "user_id": user_id,
        "ip_address": ip_address,
        "details": details or {}
    }
    
    logger.info(f"SECURITY_EVENT: {event_data}")

def log_error(error: Exception, context: str = ""):
    """
    Log error with context information
    """
    logger.error(f"ERROR in {context}: {str(error)}", exc_info=True)

def log_info(message: str, context: str = ""):
    """
    Log informational message
    """
    if context:
        logger.info(f"[{context}] {message}")
    else:
        logger.info(message)