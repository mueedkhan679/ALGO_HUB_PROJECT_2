# 🆓 Complete Setup Guide for Google Gemini (FREE)

## Step-by-Step Setup to Avoid Credit Limits

---

## 📋 Prerequisites

- Python 3.9 or higher
- A Google account (Gmail)
- **NO credit card required!**

---

## 🚀 Installation Steps

### 1. Install Dependencies

```bash
# Install all requirements including Google AI
pip install -r requirements.txt
```

This will install:
- `google-generativeai==0.3.2` - Google AI SDK
- `langchain-google-genai==0.0.6` - LangChain integration for Gemini

### 2. Get Your FREE Google API Key

1. **Visit**: https://makersuite.google.com/app/apikey
2. **Sign in** with your Google/Gmail account
3. **Click**: "Create API Key"
4. **Select** a project (or create new)
5. **Copy** your API key (looks like: `AIzaSy...`)

**Important**: 
- ✅ No credit card required
- ✅ Free forever (within limits)
- ✅ 60 requests per minute
- ✅ 1,500 requests per day

### 3. Configure .env File

Open your `.env` file and update it:

```env
# ===== LLM PROVIDER SELECTION =====
# Choose which LLM to use: "openai" or "gemini"
LLM_PROVIDER=gemini

# ===== GOOGLE GEMINI CONFIGURATION =====
# Your FREE Google API key
GOOGLE_API_KEY=AIza-your-actual-api-key-here

# ===== OPENAI CONFIGURATION (Optional - can be removed) =====
# OPENAI_API_KEY=sk-proj-...

# ===== BACKEND CONFIGURATION =====
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_RELOAD=true
BACKEND_LOG_LEVEL=info

# ===== FRONTEND CONFIGURATION =====
FRONTEND_PORT=8501
FRONTEND_SERVER_ADDRESS=localhost

# ===== API CONFIGURATION =====
API_BASE_URL=http://localhost:8000

# ===== MEMORY CONFIGURATION =====
MEMORY_STORAGE_DIR=memory_storage
```

**Key changes:**
1. Set `LLM_PROVIDER=gemini`
2. Add your `GOOGLE_API_KEY`
3. (Optional) Remove or comment out `OPENAI_API_KEY`

### 4. Create Memory Storage Directory

```bash
mkdir memory_storage
```

### 5. Restart the Backend

```bash
# Stop current backend (Ctrl+C)
python run_backend.py
```

You should see:
```
✓ Using Google Gemini (free tier)
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 6. Start the Frontend

```bash
# In a new terminal
python run_frontend.py
```

### 7. Test the Chatbot

1. Open browser: http://localhost:8501
2. Type: "What is your return policy?"
3. You should get a response from Gemini!

---

## ✅ Verification Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Google API key obtained from https://makersuite.google.com/app/apikey
- [ ] `.env` file updated with `LLM_PROVIDER=gemini`
- [ ] `.env` file updated with `GOOGLE_API_KEY=AIza...`
- [ ] `memory_storage` directory created
- [ ] Backend restarted successfully
- [ ] Backend shows "✓ Using Google Gemini (free tier)"
- [ ] Frontend started
- [ ] Chat responds to test message

---

## 🔍 Troubleshooting

### Problem: "GOOGLE_API_KEY environment variable is not set"

**Solution:**
1. Check `.env` file has `GOOGLE_API_KEY=AIza...`
2. Make sure there are no spaces around the `=` sign
3. Restart backend after changing `.env`

### Problem: "Permission denied" or "Invalid API key"

**Solution:**
1. Go to https://makersuite.google.com/app/apikey
2. Check your API key is enabled
3. Try creating a new API key
4. Make sure you're using the correct key format (`AIza...`)

### Problem: "Quota exceeded"

**Solution:**
- Free tier limits: 60 requests/minute, 1,500 requests/day
- Wait 1 minute and try again
- Check your usage at: https://makersuite.google.com/app/apikey

### Problem: Still using OpenAI

**Solution:**
1. Check `.env` has `LLM_PROVIDER=gemini` (not `openai`)
2. Restart backend completely (Ctrl+C, then `python run_backend.py`)
3. Check backend logs for "✓ Using Google Gemini (free tier)"

### Problem: Module not found errors

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade --force-reinstall -r requirements.txt
```

---

## 📊 Free Tier Limits

### Google Gemini (FREE)
- **Requests**: 60 per minute
- **Daily**: 1,500 requests per day
- **Tokens**: 1M context window
- **Cost**: $0.00 (completely free)
- **Credit Card**: NOT required

### When You Might Need More
- If you exceed 60 requests/minute → Wait or upgrade to Gemini Advanced
- If you exceed 1,500 requests/day → Wait until next day or upgrade
- For most development/testing: Free tier is MORE than enough!

---

## 🆚 Comparing OpenAI vs Gemini

| Aspect | OpenAI GPT-4o | Google Gemini 1.5 Flash |
|--------|---------------|-------------------------|
| **Cost** | $0.01-0.05/request | **FREE** |
| **Credit Card** | Required | **Not Required** |
| **Rate Limits** | 3-5 req/min (free) | **60 req/min (free)** |
| **Daily Limits** | Limited | **1,500 req/day** |
| **Quality** | 9/10 | 8.5/10 |
| **Speed** | ~2-3 sec | ~2-3 sec |
| **Setup Difficulty** | Easy | **Easy** |

**Recommendation**: Use Gemini for development/testing (free), switch to OpenAI only if you need maximum quality.

---

## 🔄 Switching Between Providers

### Switch to Gemini (FREE)
```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIza-your-key
```

### Switch to OpenAI (PAID)
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-your-key
```

**After any change**: Restart backend with `python run_backend.py`

---

## 💡 Tips for Using Gemini

### 1. **Monitor Your Usage**
Visit https://makersuite.google.com/app/apikey to see:
- Current usage
- Rate limit status
- API key management

### 2. **Optimize Requests**
- Use streaming (already enabled) to reduce token usage
- Keep conversations concise
- Clear old sessions to free up context

### 3. **Handle Rate Limits Gracefully**
The chatbot already has automatic retry logic:
- Retries up to 3 times
- Exponential backoff (1s → 2s → 4s)
- User-friendly error messages

### 4. **Test Thoroughly**
- Test all features with Gemini
- Compare response quality with OpenAI
- Ensure all prompts work correctly

---

## 📚 Additional Resources

### Google Gemini Documentation
- **Official Docs**: https://ai.google.dev/docs
- **API Reference**: https://ai.google.dev/api/python/google.generativeai
- **Free Tier Details**: https://ai.google.dev/pricing

### LangChain + Gemini
- **LangChain Docs**: https://python.langchain.com/docs/integrations/chat/google_generative_ai
- **Examples**: https://python.langchain.com/docs/integrations/chat/google_generative_ai#example

### Get Help
- **Google AI Community**: https://discuss.ai.google.dev/
- **LangChain Community**: https://discord.gg/langchain

---

## 🎯 Next Steps

1. ✅ Get your FREE Google API key
2. ✅ Update `.env` file
3. ✅ Restart backend
4. ✅ Test the chatbot
5. ✅ Enjoy FREE AI-powered support!

---

## 🆘 Need Help?

If you encounter issues:

1. **Check the logs**: Backend terminal will show error messages
2. **Verify API key**: Make sure it's correct and enabled
3. **Check .env file**: Ensure no typos or formatting issues
4. **Restart everything**: Stop and restart both backend and frontend
5. **Review this guide**: Make sure all steps are completed

---

## ✅ Success Indicators

You'll know everything is working when:

1. ✅ Backend shows: `✓ Using Google Gemini (free tier)`
2. ✅ No errors in backend logs
3. ✅ Frontend shows: `API Status: Online`
4. ✅ Chat responds to messages
5. ✅ Responses stream in real-time

---

## 🎉 Congratulations!

You've successfully switched to Google Gemini and:
- ✅ **Saved money** (no more credit card charges!)
- ✅ **Avoided rate limits** (60 req/min vs 3-5 req/min)
- ✅ **Maintained quality** (Gemini is comparable to GPT-4o)
- ✅ **Can develop freely** (no cost concerns)

**Enjoy your FREE AI-powered chatbot!** 🚀

---

*For switching back to OpenAI, see GEMINI_MIGRATION_GUIDE.md*