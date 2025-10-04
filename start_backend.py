#!/usr/bin/env python3
"""
10Q Notes AI - Backend Startup Script
HackRU 2025 Project by azrabano

Simple script to start the FastAPI backend with proper configuration
"""

import os
import sys
import uvicorn
from pathlib import Path

def start_backend():
    """Start the 10Q Notes AI FastAPI backend"""
    
    print("🚀 10Q Notes AI Backend - Starting Up")
    print("=" * 50)
    print("🎓 HackRU 2025 - Democratizing Finance Education")
    print("📚 Three Learning Modes: Learn, Practice, Feedback")
    print("🎤 ElevenLabs Voice Integration")
    print("🤖 Gemini AI Analysis Engine")
    print("=" * 50)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    backend_file = current_dir / "backend_app.py"
    
    if not backend_file.exists():
        print("❌ Error: backend_app.py not found in current directory")
        print(f"   Current directory: {current_dir}")
        print("   Please run this script from the 10q-notes-ai directory")
        sys.exit(1)
    
    # Check for environment file
    env_file = current_dir / ".env"
    if env_file.exists():
        print("✅ Environment file found")
    else:
        print("⚠️ No .env file found - using defaults")
        print("   Add .env file with API keys for full functionality:")
        print("   - GOOGLE_API_KEY=your_gemini_key")
        print("   - ELEVENLABS_API_KEY=your_elevenlabs_key")
    
    # Set up environment
    os.environ.setdefault("PYTHONPATH", str(current_dir))
    
    # Server configuration
    host = "0.0.0.0"
    port = 8000
    
    print(f"\n🌐 Starting server at http://{host}:{port}")
    print("📱 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("\n🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the FastAPI server
        uvicorn.run(
            "backend_app:app",
            host=host,
            port=port,
            reload=True,  # Enable auto-reload for development
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Backend server stopped by user")
        print("👋 Thanks for using 10Q Notes AI!")
    except Exception as e:
        print(f"\n❌ Error starting backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_backend()