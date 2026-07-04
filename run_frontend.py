"""
Run script for the Streamlit frontend application
"""

import sys
import os
import subprocess

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    print("""
╔══════════════════════════════════════════════════════════╗
║     ShopEase Customer Support Chatbot - Frontend         ║
╚══════════════════════════════════════════════════════════╝
""")
    
    print("Starting frontend server...")
    print("Chat Interface: http://localhost:8501")
    print("Press Ctrl+C to stop\n")
    
    # Run Streamlit
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "frontend/app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true"
    ])