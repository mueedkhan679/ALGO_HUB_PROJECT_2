 HEAD
# 🛍️ ShopEase Customer Support Chatbot

A production-ready, AI-powered customer support chatbot for e-commerce, built with FastAPI, Streamlit, LangChain, and OpenAI GPT-4o. Features real-time streaming responses, long-term conversation memory, and a professional chat interface.

## ✨ Features

- 🤖 **AI-Powered Support**: Powered by OpenAI GPT-4o or Google Gemini (your choice!)
- 💬 **Real-Time Streaming**: Watch responses generate in real-time for a natural conversation flow
- 🧠 **Long-Term Memory**: Conversation history persists across sessions using LangChain Memory
- 📱 **Professional UI**: Sleek, responsive Streamlit interface with modern design
- 🔄 **Session Management**: Multiple chat sessions with history tracking
- ⚠️ **Error Handling**: Graceful handling of rate limits and API errors
- 📊 **Order Tracking**: Assist customers with order status inquiries
- 🔄 **Return Policy**: Provide detailed information about returns and refunds
- 📦 **Product Queries**: Answer questions about products, availability, and specifications
- 🆓 **FREE Option**: Use Google Gemini (no credit card required!)

## 🏗️ Architecture

```
┌─────────────┐      HTTP/SSE      ┌─────────────┐      API Calls      ┌──────────┐
│  Streamlit  │ ◄────────────────► │   FastAPI   │ ◄─────────────────► │ OpenAI   │
│  Frontend   │                    │   Backend   │                     │   GPT-4o │
└─────────────┘                    └─────────────┘                     └──────────┘
                                            │
                                            │
                                    ┌───────┴───────┐
                                    │  LangChain    │
                                    │  Memory       │
                                    │  (JSON Files) │
                                    └───────────────┘
```

### Tech Stack

- **Backend**: FastAPI, Uvicorn, Pydantic
- **Frontend**: Streamlit, Custom CSS
- **AI/LLM**: OpenAI GPT-4o OR Google Gemini (your choice!)
- **Memory**: LangChain ChatMessageHistory with JSON persistence
- **Streaming**: Server-Sent Events (SSE)

## 📁 Project Structure

```
AlgoHunProject2/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI server with endpoints
│   ├── chatbot.py              # Chatbot engine with streaming
│   └── requirements.txt        # Backend dependencies
├── frontend/
│   ├── __init__.py
│   ├── app.py                  # Streamlit chat interface
│   └── requirements.txt        # Frontend dependencies
├── utils/
│   ├── __init__.py
│   ├── memory.py               # LangChain memory management
│   └── prompts.py              # System prompts and templates
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore file
├── requirements.txt            # Root requirements (all dependencies)
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- **Option A**: OpenAI API key ([Get one here](https://platform.openai.com/api-keys)) - PAID
- **Option B**: Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey)) - **FREE!**
- pip or conda for package management

### Installation

1. **Clone or download the project**
   ```bash
   cd AlgoHunProject2
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Install all dependencies
   pip install -r requirements.txt

   # OR install separately
   pip install -r backend/requirements.txt
   pip install -r frontend/requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and choose your LLM provider:
   
   # Option A: Use OpenAI (paid)
   # OPENAI_API_KEY=your_openai_api_key_here
   # LLM_PROVIDER=openai
   
   # Option B: Use Gemini (FREE - recommended!)
   # GOOGLE_API_KEY=your_google_api_key_here
   # LLM_PROVIDER=gemini
   ```

5. **Create memory storage directory**
   ```bash
   mkdir memory_storage
   ```

### Running the Application

You need to run both the backend and frontend servers.

#### 1. Start the Backend Server

```bash
# Navigate to backend directory
cd backend

# Run with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# OR run directly
python backend/main.py
```

The API will be available at `http://localhost:8000`

**API Documentation**: Visit `http://localhost:8000/docs` for interactive API docs

#### 2. Start the Frontend Server

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Run Streamlit
streamlit run frontend/app.py

# OR run from root directory
streamlit run app.py
```

The chat interface will open at `http://localhost:8501`

## 📖 Usage Guide

### Starting a Conversation

1. Open your browser to `http://localhost:8501`
2. The chat interface will load automatically
3. Type your message in the input box and press "Send" or hit Enter
4. Watch the AI response stream in real-time

### Session Management

- **New Chat**: Click "🔄 New Chat" in the sidebar to start a fresh conversation
- **Clear Session**: Click "🗑️ Clear" to clear the current session
- **Load History**: Click "📜 Load History" to reload previous messages
- **Session ID**: Each session has a unique ID displayed in the sidebar

### Example Queries

Try asking the chatbot:

- **Order Tracking**: "Where is my order SE-123456?"
- **Return Policy**: "What is your return policy?"
- **Product Query**: "Is the blue shirt available in size M?"
- **General Support**: "What payment methods do you accept?"

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | - | Yes |
| `API_BASE_URL` | Backend API URL | `http://localhost:8000` | No |
| `BACKEND_PORT` | Backend server port | `8000` | No |
| `FRONTEND_PORT` | Frontend server port | `8501` | No |
| `MEMORY_STORAGE_DIR` | Directory for memory files | `memory_storage` | No |

### Model Configuration

Edit `backend/chatbot.py` to change the LLM settings:

```python
chatbot_engine = ChatbotEngine(
    model_name="gpt-4o",      # or "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"
    temperature=0.7            # 0.0 = deterministic, 1.0 = creative
)
```

### System Prompt Customization

Edit `utils/prompts.py` to customize the chatbot's behavior:

```python
SYSTEM_PROMPT = """Your custom system prompt here..."""
```

## 🛡️ Error Handling

The chatbot includes comprehensive error handling:

- **Rate Limit Errors**: User-friendly message with suggestions
- **API Errors**: Clear error messages with contact information
- **Connection Errors**: Instructions to check backend status
- **Timeout Errors**: Prompt to retry the request

## 📊 API Endpoints

### Backend Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/chat` | POST | Send message (streaming or non-streaming) |
| `/history/{session_id}` | GET | Get chat history |
| `/clear` | POST | Clear session |
| `/session` | POST | Create/get session info |
| `/sessions` | GET | List all active sessions |

### Example API Request

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Where is my order?",
    "session_id": "your-session-id",
    "stream": true
  }'
```

## 🧪 Testing

### Test the Backend

```bash
# Health check
curl http://localhost:8000/health

# Create a session
curl -X POST "http://localhost:8000/session"

# Send a message (non-streaming)
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test", "stream": false}'
```

### Test the Frontend

1. Start both servers
2. Open `http://localhost:8501`
3. Send test messages
4. Verify streaming responses
5. Test session management features

## 🚢 Deployment

### Production Deployment

#### Backend (FastAPI)

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Frontend (Streamlit)

```bash
# Run Streamlit in production mode
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose ports
EXPOSE 8000 8501

# Run both services
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"]
```

Build and run:

```bash
docker build -t shopease-chatbot .
docker run -p 8000:8000 -p 8501:8501 -e OPENAI_API_KEY=your_key shopease-chatbot
```

### Environment Variables for Production

```env
OPENAI_API_KEY=your_production_api_key
API_BASE_URL=https://your-api-domain.com
BACKEND_RELOAD=false
BACKEND_LOG_LEVEL=warning
```

## 🔒 Security Considerations

1. **API Keys**: Never commit `.env` files to version control
2. **CORS**: Restrict `allow_origins` in production to specific domains
3. **Rate Limiting**: Implement rate limiting for production use
4. **Authentication**: Add user authentication for production deployments
5. **HTTPS**: Use HTTPS in production environments
6. **Input Validation**: All inputs are validated using Pydantic models

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem**: `ValueError: OPENAI_API_KEY environment variable is not set`
```bash
# Solution: Set your API key in .env file
echo "OPENAI_API_KEY=your_key" > .env
```

**Problem**: Port 8000 already in use
```bash
# Solution: Change port in .env or use different port
uvicorn main:app --port 8001
```

### Frontend Issues

**Problem**: `ConnectionError: Unable to connect to server`
```bash
# Solution: Ensure backend is running
# Check API_BASE_URL in .env matches backend URL
```

**Problem**: Streamlit not opening in browser
```bash
# Solution: Manually navigate to http://localhost:8501
# Or specify port: streamlit run app.py --server.port 8501
```

### Memory Issues

**Problem**: Memory not persisting
```bash
# Solution: Ensure memory_storage directory exists and has write permissions
mkdir memory_storage
chmod 755 memory_storage
```

## 📝 Development

### Adding New Features

1. **New Prompt Templates**: Add to `utils/prompts.py`
2. **New API Endpoints**: Add to `backend/main.py`
3. **New UI Components**: Add to `frontend/app.py`
4. **Memory Enhancements**: Modify `utils/memory.py`

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Add docstrings to classes and functions
- Keep functions focused and modular

## 📚 Dependencies

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **LangChain**: Framework for LLM applications
- **OpenAI**: Official OpenAI Python client
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **Streamlit**: Framework for building data apps
- **Requests**: HTTP library for API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Built as a Week 2 AI-Powered Chatbot Development project.

## 🙏 Acknowledgments

- OpenAI for GPT-4o API
- LangChain for the memory and LLM framework
- FastAPI for the excellent web framework
- Streamlit for the intuitive UI framework

## 📞 Support

For questions or issues:
- 📧 Email: support@shopease.com
- 📞 Phone: 1-800-SHOP-EASE (1-800-766-7327)
- 🕐 Hours: Monday-Friday, 9 AM - 6 PM EST

---

**Built with ❤️ for ShopEase**
=======
# ALGO_HUB_PROJECT_2
>>>>>>> ae72ac2d9c4c33573973391d11e82844e080229f
