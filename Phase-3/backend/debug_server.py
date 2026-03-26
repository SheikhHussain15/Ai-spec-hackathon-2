import os
import sys
import threading
import time
import requests
from src.main import app
import uvicorn

def run_server():
    """Run the server in a separate thread"""
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    print("Starting server in background thread...")
    
    # Start server in a background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    print("Waiting for server to start...")
    time.sleep(10)  # Wait for server to start
    
    try:
        # Test the health endpoint
        response = requests.get("http://127.0.0.1:8000/health")
        print(f"Health check response: {response.status_code}")
        print(f"Response content: {response.text}")
        
        # Test the registration endpoint
        test_data = {
            "email": "test@example.com",
            "password": "TestPass123"
        }
        reg_response = requests.post(
            "http://127.0.0.1:8000/api/auth/register",
            json=test_data
        )
        print(f"Registration response: {reg_response.status_code}")
        print(f"Registration content: {reg_response.text}")
        
    except requests.exceptions.ConnectionError:
        print("Could not connect to server - server may not have started properly")
    except Exception as e:
        print(f"Error during testing: {e}")
    
    print("Keeping server running for manual testing...")
    input("Press Enter to stop the server...")