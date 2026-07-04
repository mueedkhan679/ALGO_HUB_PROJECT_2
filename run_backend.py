"""
Run script for the FastAPI backend server
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    print("""
╔══════════════════════════════════════════════════════════╗
║     ShopEase Customer Support Chatbot - Backend          ║
╚══════════════════════════════════════════════════════════╝
""")
    
    print("Starting backend server...")
    print("API Documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop\n")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )