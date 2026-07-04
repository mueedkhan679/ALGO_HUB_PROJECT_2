"""
Setup script for E-commerce Customer Support Chatbot
This script helps with initial project setup and dependency installation
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_step(text):
    """Print a formatted step"""
    print(f"\n→ {text}")


def check_python_version():
    """Check if Python version is compatible"""
    print_step("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python 3.9+ required. Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    print_step("Setting up virtual environment...")
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("✓ Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✓ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def install_dependencies():
    """Install project dependencies"""
    print_step("Installing dependencies...")
    
    # Determine pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = ".venv\\Scripts\\pip"
    else:  # Mac/Linux
        pip_path = ".venv/bin/pip"
    
    try:
        print("  Installing backend dependencies...")
        subprocess.run(
            [pip_path, "install", "-r", "backend/requirements.txt"],
            check=True,
            capture_output=True
        )
        print("  ✓ Backend dependencies installed")
        
        print("  Installing frontend dependencies...")
        subprocess.run(
            [pip_path, "install", "-r", "frontend/requirements.txt"],
            check=True,
            capture_output=True
        )
        print("  ✓ Frontend dependencies installed")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    print_step("Creating necessary directories...")
    
    directories = [
        "memory_storage",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  ✓ Created {directory}/")
    
    return True


def setup_env_file():
    """Setup .env file from .env.example"""
    print_step("Setting up environment configuration...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("  ✓ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ .env.example not found")
        return False
    
    # Copy .env.example to .env
    with open(env_example, 'r') as f:
        content = f.read()
    
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("  ✓ Created .env file from .env.example")
    print("  ⚠️  Please edit .env and add your OPENAI_API_KEY")
    return True


def run_import_test():
    """Run the import test script"""
    print_step("Running import verification test...")
    
    # Determine python path based on OS
    if os.name == 'nt':  # Windows
        python_path = ".venv\\Scripts\\python"
    else:  # Mac/Linux
        python_path = ".venv/bin/python"
    
    try:
        result = subprocess.run(
            [python_path, "test_imports.py"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Import test failed:")
        print(e.stdout)
        print(e.stderr)
        return False


def print_next_steps():
    """Print instructions for next steps"""
    print_header("🎉 Setup Complete!")
    
    print("""
Next steps:

1. Configure your OpenAI API key:
   - Open .env file in a text editor
   - Replace 'your_openai_api_key_here' with your actual API key
   - Get your API key from: https://platform.openai.com/api-keys

2. Activate the virtual environment:
   
   Windows:
       .venv\\Scripts\\activate
   
   Mac/Linux:
       source .venv/bin/activate

3. Start the backend server (Terminal 1):
       cd backend
       uvicorn main:app --reload --port 8000
   
   Or use the run script:
       python run_backend.py

4. Start the frontend server (Terminal 2):
       cd frontend
       streamlit run frontend/app.py
   
   Or use the run script:
       python run_frontend.py

5. Open your browser:
       http://localhost:8501

📚 Documentation:
   - Full guide: README.md
   - API docs: http://localhost:8000/docs (when backend is running)

🆘 Troubleshooting:
   - If you encounter import errors, run: pip install -r requirements.txt
   - If ports are in use, modify .env to use different ports
   - Check logs/ directory for error logs

💡 Tips:
   - Keep both terminals running while using the chatbot
   - The chat history is saved in memory_storage/
   - Use Ctrl+C to stop the servers

Happy chatting! 🛍️
""")


def main():
    """Main setup function"""
    print_header("🛍️ ShopEase Chatbot Setup")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("\n❌ Setup failed at virtual environment creation")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n❌ Setup failed at directory creation")
        sys.exit(1)
    
    # Setup .env file
    if not setup_env_file():
        print("\n❌ Setup failed at environment configuration")
        sys.exit(1)
    
    # Run import test
    if not run_import_test():
        print("\n⚠️  Import test failed, but setup completed")
        print("You may need to manually install missing dependencies")
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)