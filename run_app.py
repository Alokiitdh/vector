#!/usr/bin/env python3
"""
Launch script for running both FastAPI backend and Streamlit frontend
"""

import subprocess
import sys
import time
import threading
import os
from pathlib import Path

def run_fastapi():
    """Run the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("FastAPI server stopped.")
    except Exception as e:
        print(f"Error running FastAPI: {e}")

def run_streamlit():
    """Run the Streamlit app"""
    print("🎨 Starting Streamlit app...")
    time.sleep(3)  # Wait for FastAPI to start
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], check=True)
    except KeyboardInterrupt:
        print("Streamlit app stopped.")
    except Exception as e:
        print(f"Error running Streamlit: {e}")

def main():
    """Launch both servers"""
    print("🔍 VECTOR Product Research Agent")
    print("=================================")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found. Make sure you have your API keys configured.")
        print("   Create a .env file with:")
        print("   OPENAI_API_KEY=your_openai_key")
        print("   EXA_API_KEY=your_exa_key")
        print("")
    
    try:
        # Start FastAPI in a separate thread
        fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
        fastapi_thread.start()
        
        # Start Streamlit (this will block)
        run_streamlit()
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()