import uvicorn
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Import the app
from src.main import app

if __name__ == "__main__":
    print("Starting backend server on port 8000...")
    print("Press Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="info",
            reload=False
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()