# 🔧 Environment Variable Loading Fix

## Problem

The backend was throwing `ValueError: OPENAI_API_KEY environment variable is not set` even though the `.env` file existed and contained the API key.

## Root Cause

The issue was **import order** in `backend/main.py`:

### Before (Broken):
```python
# Line 14: Import chatbot_engine
from backend.chatbot import chatbot_engine  # ❌ Triggers ChatbotEngine() initialization

# Line 262: load_dotenv() called HERE (too late!)
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
```

**What happened:**
1. `backend/main.py` imports `chatbot_engine` on line 14
2. This triggers `backend/chatbot.py` to load
3. `backend/chatbot.py` has `chatbot_engine = ChatbotEngine()` at module level (line 262)
4. `ChatbotEngine.__init__()` calls `os.getenv("OPENAI_API_KEY")` 
5. **ERROR**: `.env` file hasn't been loaded yet!

---

## Solution

Move `load_dotenv()` to the **top of the file**, **before** any imports that need environment variables:

### After (Fixed):
```python
# Line 11: Import load_dotenv
from dotenv import load_dotenv

# Line 14: Load .env BEFORE importing chatbot
load_dotenv()  # ✅ Loads .env first

# Line 16: Now safe to import chatbot_engine
from backend.chatbot import chatbot_engine
```

---

## Changes Made

### File: `backend/main.py`

**Change 1:** Added `load_dotenv()` import and call at the top
```python
from dotenv import load_dotenv

# Load environment variables BEFORE importing modules that need them
load_dotenv()

from backend.chatbot import chatbot_engine
```

**Change 2:** Removed duplicate `load_dotenv()` from `__main__` block
```python
if __name__ == "__main__":
    import uvicorn
    # Removed: from dotenv import load_dotenv
    # Removed: load_dotenv()
    
    uvicorn.run(...)
```

---

## How It Works Now

### Correct Execution Order:
1. `backend/main.py` starts loading
2. **Line 11**: Import `load_dotenv`
3. **Line 14**: Call `load_dotenv()` - loads `.env` file
4. **Line 16**: Import `chatbot_engine` - now safe!
5. `backend/chatbot.py` loads
6. **Line 262**: `ChatbotEngine()` initializes
7. `os.getenv("OPENAI_API_KEY")` - **SUCCESS** - key is available!

---

## Verification

### Step 1: Verify .env file exists
```bash
# In project root (d:/AlgoHunProject2)
ls -la .env
```

Should show the file with your API key.

### Step 2: Restart backend
```bash
# Stop current backend (Ctrl+C)
python run_backend.py
```

### Step 3: Check for success message
You should see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**No more `ValueError: OPENAI_API_KEY environment variable is not set`!**

### Step 4: Test the API
```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "ShopEase Chatbot API",
  "version": "1.0.0"
}
```

---

## Alternative: Explicit .env Path

If you're still having issues, you can specify the `.env` file path explicitly:

```python
from dotenv import load_dotenv
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"

# Load .env from project root
load_dotenv(dotenv_path=env_path)
```

This ensures `load_dotenv()` looks for `.env` in the project root, regardless of where the script is run from.

---

## Common Issues & Solutions

### Issue 1: ".env file not found"
**Solution:** Make sure `.env` is in the project root (`d:/AlgoHunProject2/.env`)

### Issue 2: "API key still not found"
**Solution:** Check `.env` file format:
```bash
# Correct format:
OPENAI_API_KEY=sk-proj-...

# Wrong formats:
OPENAI_API_KEY = sk-proj-...  # ❌ No spaces around =
export OPENAI_API_KEY=sk-...  # ❌ No 'export' keyword
```

### Issue 3: "Changes not taking effect"
**Solution:** 
1. Stop the backend server completely (Ctrl+C)
2. Start it fresh: `python run_backend.py`
3. Don't just reload - restart completely

---

## Best Practices

### 1. **Load .env as early as possible**
Always load environment variables at the top of your entry point file, before any other imports.

### 2. **Use a single entry point**
Have one main file that loads `.env` and then imports other modules.

### 3. **Don't rely on `__main__` block**
The `if __name__ == "__main__"` block only runs when the file is executed directly, not when imported. Always load `.env` at module level.

### 4. **Verify with a test**
Add a simple check after `load_dotenv()`:
```python
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("WARNING: OPENAI_API_KEY not found!")
else:
    print("✓ OPENAI_API_KEY loaded successfully")
```

---

## Testing the Fix

### Quick Test:
```bash
# Terminal 1: Start backend
python run_backend.py

# Should see:
# ✓ OPENAI_API_KEY loaded successfully
# INFO:     Application startup complete.

# Terminal 2: Test API
curl http://localhost:8000/health

# Should return healthy status
```

### Full Integration Test:
1. Start backend: `python run_backend.py`
2. Start frontend: `python run_frontend.py`
3. Open http://localhost:8501
4. Send a message: "Hello"
5. Should get AI response (no API key error!)

---

## Summary

**Problem:** `.env` file was loaded too late (after importing modules that needed it)

**Solution:** Moved `load_dotenv()` to the top of `backend/main.py`, before importing `chatbot_engine`

**Result:** Environment variables are now loaded before `ChatbotEngine` initializes, so `os.getenv("OPENAI_API_KEY")` works correctly

**Status:** ✅ Fixed and ready to test!

Restart your backend server to apply the fix:
```bash
python run_backend.py