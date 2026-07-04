# 🚀 How to Run the ShopEase Chatbot

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Key
```bash
# Copy environment template
copy .env.example .env

# Edit .env file and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 3: Run the Application

You need **TWO terminal windows**:

**Terminal 1 - Backend:**
```bash
python run_backend.py
```
✅ Backend running at: http://localhost:8000

**Terminal 2 - Frontend:**
```bash
python run_frontend.py
```
✅ Frontend running at: http://localhost:8501

**Open your browser:** http://localhost:8501

---

## Alternative: Manual Setup

### 1. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Required Directories
```bash
mkdir memory_storage logs
```

### 4. Configure Environment
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env

# Edit .env and add your OpenAI API key
```

### 5. Start Backend Server
```bash
# Option A: Using run script
python run_backend.py

# Option B: Using uvicorn directly
cd backend
uvicorn main:app --reload --port 8000

# Option C: Using Python module
python -m uvicorn backend.main:app --reload --port 8000
```

### 6. Start Frontend Server (New Terminal)
```bash
# Option A: Using run script
python run_frontend.py

# Option B: Using streamlit directly
cd frontend
streamlit run frontend/app.py

# Option C: From root directory
streamlit run frontend/app.py --server.port 8501
```

---

## Verify Installation

Run the import test to check if everything is installed correctly:
```bash
python test_imports.py
```

Expected output: ✅ All imports successful!

---

## Using the Chatbot

1. **Open Browser**: Navigate to http://localhost:8501
2. **Start Chatting**: Type your message in the input box
3. **Watch Streaming**: See the AI response generate in real-time
4. **Session Management**: Use sidebar buttons to manage sessions
   - 🔄 New Chat - Start fresh conversation
   - 🗑️ Clear - Clear current session
   - 📜 Load History - Reload previous messages

---

## Example Queries to Try

- "Where is my order SE-123456?"
- "What is your return policy?"
- "Is the blue shirt available in size M?"
- "What payment methods do you accept?"
- "How long does shipping take?"

---

## Troubleshooting

### Problem: "ModuleNotFoundError"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Problem: "OPENAI_API_KEY not set"
```bash
# Solution: Add your API key to .env file
# Get key from: https://platform.openai.com/api-keys
```

### Problem: "Port 8000 already in use"
```bash
# Solution: Use different port
uvicorn backend.main:app --reload --port 8001
# Then update API_BASE_URL in .env to http://localhost:8001
```

### Problem: "Connection refused" in frontend
```bash
# Solution: Ensure backend is running first
# Check API_BASE_URL in .env matches backend URL
```

### Problem: "Memory not persisting"
```bash
# Solution: Create memory directory
mkdir memory_storage
```

---

## Stopping the Application

Press `Ctrl+C` in each terminal to stop the servers.

---

## Next Steps

- Read the full documentation: [README.md](README.md)
- Explore the API: http://localhost:8000/docs
- Customize the system prompt: `utils/prompts.py`
- Adjust model settings: `backend/chatbot.py`

---

## Need Help?

- 📧 Email: support@shopease.com
- 📞 Phone: 1-800-SHOP-EASE
- 📚 Full Guide: README.md

**Happy Chatting! 🛍️**