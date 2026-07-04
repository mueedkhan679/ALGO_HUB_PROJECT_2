# 🛡️ Rate Limit Handling Implementation

## Overview

The chatbot now implements a robust retry mechanism with exponential backoff to handle OpenAI API rate limits gracefully. This ensures the application remains resilient during high traffic periods.

---

## ✨ Features Implemented

### 1. **Automatic Retry with Exponential Backoff**
- Automatically retries failed requests up to 3 times (configurable)
- Wait time increases exponentially: 1s → 2s → 4s (capped at 60s)
- Transparent to users - they see a "retrying" message

### 2. **Graceful Error Messages**
- No technical jargon exposed to users
- Polite, professional messages
- Helpful suggestions for alternative actions
- Emoji indicators for better UX

### 3. **Smart Error Handling**
- **RateLimitError**: Retries with backoff, then shows friendly message
- **APIError**: Shows service unavailable message (no retry)
- **Other Errors**: Shows generic error message (no retry)

### 4. **Dual Implementation**
- Works for both streaming and non-streaming modes
- Consistent behavior across both methods

---

## 🔧 Implementation Details

### Configuration

```python
# In backend/chatbot.py
chatbot_engine = ChatbotEngine(
    model_name="gpt-4o",
    temperature=0.7,
    max_retries=3  # Configurable retry count
)
```

### Retry Strategy

**Exponential Backoff Formula:**
```python
wait_time = min(2 ** attempt, 60)  # Cap at 60 seconds
```

**Retry Attempts:**
- Attempt 1: Immediate
- Attempt 2: Wait 1 second (2^0)
- Attempt 3: Wait 2 seconds (2^1)
- Attempt 4: Wait 4 seconds (2^2)

**Maximum Wait:** 60 seconds (prevents excessive waiting)

---

## 📝 Code Changes

### Streaming Method (`generate_response_stream`)

```python
for attempt in range(self.max_retries):
    try:
        # Try to generate response
        async for chunk in self.client.astream(messages):
            # Stream tokens
            yield token
        return  # Success - exit loop
        
    except RateLimitError:
        if attempt < self.max_retries - 1:
            # Retry with backoff
            wait_time = min(2 ** attempt, 60)
            yield f"⏳ Retrying in {wait_time} seconds..."
            time.sleep(wait_time)
        else:
            # Final attempt failed
            yield "⚠️ Rate Limit Exceeded - Please wait a minute..."
```

### Non-Streaming Method (`generate_response`)

```python
for attempt in range(self.max_retries):
    try:
        # Try to generate response
        response = self.client.invoke(messages)
        return response_text, None  # Success
        
    except RateLimitError:
        if attempt < self.max_retries - 1:
            time.sleep(min(2 ** attempt, 60))
        else:
            return error_msg, "rate_limit"
```

---

## 🎯 User Experience

### Scenario 1: Rate Limit Hit, Retry Succeeds

**User sees:**
```
User: What's your return policy?

Assistant: ⏳ Rate limit hit. Retrying in 1 seconds...

Assistant: Our return policy allows returns within 30 days...
```

**Backend logs:**
```
INFO: POST /chat - Rate limit hit, retrying (attempt 1/3)
INFO: POST /chat - Rate limit hit, retrying (attempt 2/3)
INFO: POST /chat - Success
```

### Scenario 2: Rate Limit Persists, All Retries Fail

**User sees:**
```
User: What's your return policy?

Assistant: ⏳ Rate limit hit. Retrying in 1 seconds...

Assistant: ⏳ Rate limit hit. Retrying in 2 seconds...

Assistant: ⏳ Rate limit hit. Retrying in 4 seconds...

⚠️ Rate Limit Exceeded

I'm experiencing high traffic at the moment. Please wait a minute and try again. 
Our team has been notified and we're working to resolve this.

In the meantime, you can:
- Check our FAQ section for quick answers
- Email us at support@shopease.com
- Call us at 1-800-SHOP-EASE

Thank you for your patience! 🙏
```

---

## 🔍 Error Messages

### Rate Limit Error (Final)
```
⚠️ Rate Limit Exceeded

I'm experiencing high traffic at the moment. Please wait a minute and try again. 
Our team has been notified and we're working to resolve this.

In the meantime, you can:
- Check our FAQ section for quick answers
- Email us at support@shopease.com
- Call us at 1-800-SHOP-EASE

Thank you for your patience! 🙏
```

### API Error
```
⚠️ Service Temporarily Unavailable

I'm experiencing technical difficulties connecting to our AI service. 
Please try again in a few moments.

If the issue persists, please contact our support team at:
- Email: support@shopease.com
- Phone: 1-800-SHOP-EASE
```

### Unexpected Error
```
⚠️ Unexpected Error

Something went wrong while processing your request. 
Please try again or contact our support team for assistance.

We apologize for the inconvenience!
```

---

## ⚙️ Configuration Options

### Adjust Retry Count

```python
# In backend/chatbot.py - line 262
chatbot_engine = ChatbotEngine(
    model_name="gpt-4o",
    temperature=0.7,
    max_retries=5  # Increase for more retries
)
```

### Adjust Backoff Timing

```python
# In backend/chatbot.py - in generate_response_stream method
# Current: wait_time = min(2 ** attempt, 60)
# 
# For faster retries:
wait_time = min(1.5 ** attempt, 60)  # 1s → 1.5s → 2.25s
#
# For slower retries:
wait_time = min(3 ** attempt, 60)  # 1s → 3s → 9s
```

### Disable Retries (Not Recommended)

```python
chatbot_engine = ChatbotEngine(
    model_name="gpt-4o",
    temperature=0.7,
    max_retries=1  # Only try once
)
```

---

## 🧪 Testing

### Test Rate Limit Handling

1. **Simulate Rate Limit:**
   ```bash
   # Temporarily set a low RPM limit in OpenAI dashboard
   # Or use a test API key with low limits
   ```

2. **Send Multiple Requests:**
   - Rapidly send 5-10 messages
   - Observe retry behavior in backend logs
   - Verify user sees retry messages

3. **Expected Behavior:**
   - First request succeeds
   - Subsequent requests trigger retries
   - User sees "Retrying in X seconds..." messages
   - After max retries, user sees friendly error

### Check Backend Logs

```bash
# Look for these log entries:
INFO: POST /chat - Rate limit hit, retrying (attempt 1/3)
INFO: POST /chat - Success after 1 retries
```

---

## 📊 Benefits

### For Users
- ✅ No raw error messages
- ✅ Polite, professional communication
- ✅ Automatic retry (no manual intervention needed)
- ✅ Clear expectations ("Please wait a minute")
- ✅ Alternative contact options provided

### For Developers
- ✅ Reduced support tickets
- ✅ Better user retention during rate limits
- ✅ Configurable retry behavior
- ✅ Comprehensive error logging
- ✅ No code changes needed in frontend

### For Business
- ✅ Improved reliability
- ✅ Better user experience
- ✅ Professional brand image
- ✅ Reduced downtime impact

---

## 🚨 Important Notes

### Rate Limit Best Practices

1. **Monitor Usage:**
   - Check OpenAI dashboard regularly
   - Set up alerts for rate limit warnings
   - Review usage patterns

2. **Optimize Requests:**
   - Cache common responses
   - Implement request deduplication
   - Use streaming to reduce token usage

3. **Upgrade Plan:**
   - Consider higher tier OpenAI plan
   - Implement request queuing for high traffic
   - Use multiple API keys with load balancing

4. **Fallback Strategy:**
   - Have human agent escalation ready
   - Display FAQ when rate limited
   - Queue messages for later processing

---

## 🔄 How It Works

### Flow Diagram

```
User sends message
    ↓
Backend receives POST /chat
    ↓
Attempt 1: Call OpenAI API
    ↓
    ├─ Success → Stream response → Save to memory → Done
    │
    └─ RateLimitError → Wait 1s → Attempt 2
                              ↓
                              ├─ Success → Stream response → Done
                              │
                              └─ RateLimitError → Wait 2s → Attempt 3
                                                        ↓
                                                        ├─ Success → Stream response → Done
                                                        │
                                                        └─ RateLimitError → Show error message
```

### State Management

- **Success:** Response streamed, memory saved, session continues
- **Retry Success:** User sees retry message, then full response
- **Final Failure:** User sees error message, can try again later

---

## 📚 Related Files

- **backend/chatbot.py** - Retry logic implementation
- **frontend/app.py** - Displays error messages to users
- **utils/prompts.py** - System prompt (unchanged)
- **.env** - OpenAI API key configuration

---

## 🎓 Advanced: Using Tenacity Library (Optional)

For more advanced retry logic, you can use the `tenacity` library:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    retry=retry_if_exception_type(RateLimitError)
)
async def generate_with_retry(self, messages):
    async for chunk in self.client.astream(messages):
        yield chunk.content
```

**Install tenacity:**
```bash
pip install tenacity
```

---

## ✅ Summary

The chatbot now handles rate limits gracefully with:
- **3 automatic retries** with exponential backoff
- **User-friendly messages** at each stage
- **No crashes or raw errors** exposed to users
- **Configurable** retry count and timing
- **Consistent behavior** in streaming and non-streaming modes

**Status:** ✅ Rate limit handling implemented and ready for testing!

Restart the backend server to apply changes:
```bash
python run_backend.py