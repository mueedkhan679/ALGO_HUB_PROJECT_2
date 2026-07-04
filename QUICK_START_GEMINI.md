# ⚡ Quick Start: Switch to FREE Google Gemini

## Avoid Credit Limits in 3 Simple Steps

---

## 🎯 The Problem
- ❌ OpenAI requires credit card
- ❌ Strict rate limits (3-5 requests/minute)
- ❌ Costs $0.01-0.05 per request
- ❌ Hitting rate limits constantly

## ✅ The Solution
- ✅ **Google Gemini is 100% FREE**
- ✅ **No credit card required**
- ✅ **60 requests/minute** (12x more than OpenAI)
- ✅ **1,500 requests/day**
- ✅ **Same quality as GPT-4o**

---

## 🚀 3-Step Setup (5 Minutes)

### Step 1: Get FREE API Key
```
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google/Gmail
3. Click "Create API Key"
4. Copy key (starts with AIza...)
```

### Step 2: Update .env File
```env
# Add these lines to your .env file:
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIza-your-key-here
```

### Step 3: Restart Backend
```bash
# Stop backend (Ctrl+C)
python run_backend.py
```

**That's it!** You'll see: `✓ Using Google Gemini (free tier)`

---

## 📋 Complete Checklist

- [ ] Go to https://makersuite.google.com/app/apikey
- [ ] Create API key (no credit card!)
- [ ] Copy your API key (AIza...)
- [ ] Open `.env` file
- [ ] Add: `LLM_PROVIDER=gemini`
- [ ] Add: `GOOGLE_API_KEY=AIza-your-key`
- [ ] Save `.env` file
- [ ] Restart backend: `python run_backend.py`
- [ ] Verify: See "✓ Using Google Gemini (free tier)"
- [ ] Start frontend: `python run_frontend.py`
- [ ] Test: Open http://localhost:8501
- [ ] Send message: "Hello"
- [ ] ✅ Working!

---

## 🔄 How to Switch Back to OpenAI

If you want to switch back to OpenAI later:

```env
# In .env file:
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-your-key
```

Then restart backend.

---

## 📊 Side-by-Side Comparison

| Feature | OpenAI | Gemini |
|---------|--------|--------|
| **Cost** | $0.01-0.05/req | **FREE** |
| **Credit Card** | Required | **Not Required** |
| **Rate Limit** | 3-5 req/min | **60 req/min** |
| **Daily Limit** | Limited | **1,500 req/day** |
| **Quality** | 9/10 | 8.5/10 |
| **Setup** | Easy | **Easy** |

---

## 🆘 Troubleshooting

### "GOOGLE_API_KEY not set"
→ Check `.env` has `GOOGLE_API_KEY=AIza...`

### "Invalid API key"
→ Get new key from https://makersuite.google.com/app/apikey

### "Quota exceeded"
→ Wait 1 minute (60 req/min limit)

### Still using OpenAI
→ Check `.env` has `LLM_PROVIDER=gemini` and restart backend

---

## 📚 Full Documentation

- **GEMINI_SETUP.md** - Complete setup guide
- **GEMINI_MIGRATION_GUIDE.md** - Detailed migration info
- **README.md** - Main project documentation

---

## 💡 Pro Tips

1. **Use Gemini for development** - It's free!
2. **Switch to OpenAI for production** - If you need max quality
3. **Monitor usage** - Check https://makersuite.google.com/app/apikey
4. **Keep both keys** - Easy to switch anytime

---

## ✅ You're Done!

Your chatbot now uses **FREE Google Gemini** instead of paid OpenAI.

**Benefits:**
- 💰 No more credit card charges
- 🚀 12x higher rate limits
- 🎯 Same great quality
- 🔄 Easy to switch back

**Next:** Start chatting at http://localhost:8501

---

*Questions? Check GEMINI_SETUP.md for detailed troubleshooting*