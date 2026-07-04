"""
FastAPI Backend Server
Provides REST API endpoints for the chatbot with streaming support
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables BEFORE importing modules that need them
load_dotenv()

# Import both chatbot engines
from backend.chatbot import chatbot_engine as openai_engine
from backend.chatbot_gemini import gemini_chatbot_engine

# Select which engine to use based on environment variable
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
if LLM_PROVIDER == "gemini":
    chatbot_engine = gemini_chatbot_engine
    print("✓ Using Google Gemini (free tier)")
else:
    chatbot_engine = openai_engine
    print("✓ Using OpenAI GPT-4o")

from utils.memory import memory_manager

# Initialize FastAPI app
app = FastAPI(
    title="ShopEase Customer Support Chatbot API",
    description="API for E-commerce Customer Support Chatbot with streaming support",
    version="1.0.0"
)

# Configure CORS to allow Streamlit frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    session_id: Optional[str] = None
    stream: bool = True


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    session_id: str
    timestamp: str
    error: Optional[str] = None


class SessionRequest(BaseModel):
    """Session management request"""
    session_id: Optional[str] = None


class SessionResponse(BaseModel):
    """Session management response"""
    session_id: str
    message_count: int
    created_at: str


class HistoryResponse(BaseModel):
    """Chat history response"""
    session_id: str
    messages: List[dict]
    message_count: int


class ClearResponse(BaseModel):
    """Clear session response"""
    session_id: str
    message: str
    success: bool


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ShopEase Chatbot API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


# Chat endpoint with streaming support
@app.post("/chat", tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Main chat endpoint that processes user messages and returns responses.
    Supports both streaming and non-streaming modes.
    """
    try:
        # Generate or use provided session ID
        session_id = request.session_id or str(uuid.uuid4())
        
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        if request.stream:
            # Return streaming response
            from fastapi.responses import StreamingResponse
            import json
            
            async def generate():
                try:
                    async for token in chatbot_engine.generate_response_stream(session_id, request.message):
                        # Format as Server-Sent Events
                        yield f"data: {json.dumps({'token': token, 'session_id': session_id})}\n\n"
                    yield f"data: [DONE]\n\n"
                except Exception as e:
                    error_data = json.dumps({'error': str(e), 'session_id': session_id})
                    yield f"data: {error_data}\n\n"
            
            return StreamingResponse(
                generate(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Session-ID": session_id
                }
            )
        else:
            # Return non-streaming response
            response_text, error = chatbot_engine.generate_response(session_id, request.message)
            
            if error:
                return ChatResponse(
                    response=response_text,
                    session_id=session_id,
                    timestamp=datetime.now().isoformat(),
                    error=error
                )
            
            return ChatResponse(
                response=response_text,
                session_id=session_id,
                timestamp=datetime.now().isoformat()
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Get chat history
@app.get("/history/{session_id}", response_model=HistoryResponse, tags=["Session"])
async def get_history(session_id: str):
    """
    Get chat history for a specific session.
    """
    try:
        messages = chatbot_engine.get_conversation_history(session_id)
        
        return HistoryResponse(
            session_id=session_id,
            messages=messages,
            message_count=len(messages)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")


# Clear session
@app.post("/clear", response_model=ClearResponse, tags=["Session"])
async def clear_session(request: SessionRequest):
    """
    Clear chat history for a session.
    """
    try:
        if not request.session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")
        
        success = chatbot_engine.clear_conversation(request.session_id)
        
        return ClearResponse(
            session_id=request.session_id,
            message="Session cleared successfully" if success else "Failed to clear session",
            success=success
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing session: {str(e)}")


# Create new session
@app.post("/session", response_model=SessionResponse, tags=["Session"])
async def create_session(request: SessionRequest):
    """
    Create a new chat session or get info about existing session.
    """
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get or create session
        memory_manager.get_or_create_session(session_id)
        
        # Get message count
        history = chatbot_engine.get_conversation_history(session_id)
        
        return SessionResponse(
            session_id=session_id,
            message_count=len(history),
            created_at=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")


# Get all active sessions (for debugging/admin purposes)
@app.get("/sessions", tags=["Session"])
async def get_sessions():
    """
    Get list of all active sessions (for debugging).
    """
    try:
        sessions = []
        for session_id in memory_manager.sessions.keys():
            history = chatbot_engine.get_conversation_history(session_id)
            sessions.append({
                "session_id": session_id,
                "message_count": len(history)
            })
        
        return {
            "sessions": sessions,
            "total_sessions": len(sessions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sessions: {str(e)}")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "service": "ShopEase Customer Support Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "history": "/history/{session_id}",
            "clear": "/clear",
            "session": "/session",
            "sessions": "/sessions"
        },
        "documentation": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
