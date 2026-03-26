import uvicorn
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Import the app
from src.main import app

if __name__ == "__main__":
    print("Starting server with uvicorn...", flush=True)
    
    # Run the server with logging to file
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        reload=False,
        access_log=True
    )