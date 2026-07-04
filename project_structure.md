# E-commerce Customer Support Chatbot - Project Structure

```
AlgoHunProject2/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI backend server
│   ├── chatbot.py              # Chatbot logic and LLM integration
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
└── README.md                   # Setup and deployment guide
```

## Application Flow

1. **User Interaction**: User opens Streamlit frontend and sends a message
2. **API Call**: Frontend sends message to FastAPI backend via HTTP POST
3. **Memory Retrieval**: Backend loads conversation history from LangChain memory
4. **LLM Processing**: Backend constructs prompt with system message + history + user message
5. **Streaming Response**: Backend streams GPT-4o response back to frontend in real-time
6. **Memory Update**: Backend saves the conversation exchange to memory
7. **UI Display**: Frontend displays streaming response to user
8. **Error Handling**: RateLimitError caught and displayed gracefully

## Key Features
- Real-time streaming responses
- Conversation memory across sessions
- Rate limit handling with user-friendly messages
- Professional chat UI with session management
- Modular, production-ready code structure