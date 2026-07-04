"""
Streamlit Frontend Application
Professional chat interface for the E-commerce Customer Support Chatbot
"""

import streamlit as st
import os 
import requests
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict
import time

# Page configuration
st.set_page_config(
    page_title="ShopEase Customer Support",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main chat container */
    .main-chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 15px 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        max-width: 80%;
        word-wrap: break-word;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        text-align: right;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        background: #f8f9fa;
        color: #333;
        margin-right: auto;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Input area styling */
    .input-container {
        display: flex;
        gap: 10px;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        position: sticky;
        bottom: 0;
        margin-top: 20px;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Status indicator */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 5px;
        animation: pulse 2s infinite;
    }
    
    .status-online {
        background-color: #28a745;
    }
    
    .status-offline {
        background-color: #dc3545;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        gap: 5px;
        padding: 10px 15px;
        background: #f8f9fa;
        border-radius: 15px;
        width: fit-content;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #999;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }
    
    /* Error message styling */
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin-bottom: 15px;
    }
    
    /* Success message styling */
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)


# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "api_status" not in st.session_state:
        st.session_state.api_status = "unknown"
    
    if "is_typing" not in st.session_state:
        st.session_state.is_typing = False


def check_api_health() -> bool:
    """
    Check if the backend API is healthy.
    
    Returns:
        True if API is healthy, False otherwise
    """
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            st.session_state.api_status = "online"
            return True
    except:
        pass
    
    st.session_state.api_status = "offline"
    return False


def send_message(message: str, session_id: str, stream: bool = True):
    """
    Send a message to the chatbot API.
    
    Args:
        message: User's message
        session_id: Chat session ID
        stream: Whether to use streaming mode
        
    Yields:
        Response tokens (streaming) or full response (non-streaming)
    """
    try:
        payload = {
            "message": message,
            "session_id": session_id,
            "stream": stream
        }
        
        if stream:
            # Streaming mode
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json=payload,
                stream=True,
                timeout=60
            )
            
            if response.status_code == 200:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = line[6:]  # Remove 'data: ' prefix
                            if data == '[DONE]':
                                break
                            try:
                                json_data = json.loads(data)
                                if 'token' in json_data:
                                    token = json_data['token']
                                    full_response += token
                                    yield token
                                elif 'error' in json_data:
                                    yield f"\n\n⚠️ **Error**: {json_data['error']}"
                                    return
                            except json.JSONDecodeError:
                                continue
            else:
                yield f"\n\n⚠️ **Error**: Server returned status {response.status_code}"
        else:
            # Non-streaming mode
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                yield data.get("response", "No response received")
            else:
                yield f"⚠️ **Error**: Server returned status {response.status_code}"
    
    except requests.exceptions.Timeout:
        yield "⚠️ **Timeout**: The request took too long. Please try again."
    
    except requests.exceptions.ConnectionError:
        yield "⚠️ **Connection Error**: Unable to connect to the server. Please ensure the backend is running."
    
    except Exception as e:
        yield f"⚠️ **Error**: {str(e)}"


def load_chat_history(session_id: str) -> List[Dict]:
    """
    Load chat history from the API.
    
    Args:
        session_id: Chat session ID
        
    Returns:
        List of messages
    """
    try:
        response = requests.get(f"{API_BASE_URL}/history/{session_id}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("messages", [])
    except:
        pass
    
    return []


def clear_chat_session(session_id: str) -> bool:
    """
    Clear chat session via API.
    
    Args:
        session_id: Chat session ID
        
    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/clear",
            json={"session_id": session_id},
            timeout=10
        )
        return response.status_code == 200
    except:
        return False


def render_chat_message(role: str, content: str, timestamp: Optional[str] = None):
    """
    Render a chat message with proper styling.
    
    Args:
        role: Message role ('user' or 'assistant')
        content: Message content
        timestamp: Optional timestamp
    """
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You</strong>
            <p>{content}</p>
            {f'<small style="opacity: 0.7;">{timestamp}</small>' if timestamp else ''}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🛍️ ShopEase Assistant</strong>
            <div>{content}</div>
            {f'<small style="opacity: 0.6;">{timestamp}</small>' if timestamp else ''}
        </div>
        """, unsafe_allow_html=True)


def render_typing_indicator():
    """Render typing indicator"""
    st.markdown("""
    <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with session information and controls"""
    with st.sidebar:
        st.title("🛍️ ShopEase Support")
        
        # API Status
        st.markdown("### System Status")
        is_healthy = check_api_health()
        status_class = "status-online" if is_healthy else "status-offline"
        status_text = "Online" if is_healthy else "Offline"
        
        st.markdown(f"""
        <div style="padding: 10px; background: white; border-radius: 8px; margin-bottom: 15px;">
            <span class="status-indicator {status_class}"></span>
            <strong>API Status: {status_text}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Session Information
        st.markdown("### Session Information")
        st.markdown(f"""
        <div class="sidebar-section">
            <p><strong>Session ID:</strong></p>
            <code style="font-size: 10px; word-break: break-all;">{st.session_state.session_id[:16]}...</code>
        </div>
        """, unsafe_allow_html=True)
        
        # Message count
        message_count = len(st.session_state.messages)
        st.metric("Messages", message_count)
        
        # Actions
        st.markdown("### Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 New Chat", use_container_width=True):
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                if clear_chat_session(st.session_state.session_id):
                    st.session_state.messages = []
                    st.success("Session cleared!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to clear session")
        
        # Load history button
        if st.button("📜 Load History", use_container_width=True):
            with st.spinner("Loading history..."):
                history = load_chat_history(st.session_state.session_id)
                if history:
                    st.session_state.messages = history
                    st.success(f"Loaded {len(history)} messages")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.info("No history found for this session")
        
        # Information
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        <div class="sidebar-section">
            <p>This is an AI-powered customer support chatbot for ShopEase.</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Order tracking</li>
                <li>Return policy info</li>
                <li>Product queries</li>
                <li>24/7 support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<small style='text-align: center; color: #666;'>Powered by GPT-4o</small>", 
                   unsafe_allow_html=True)


def render_chat_interface():
    """Render the main chat interface"""
    st.title("💬 Customer Support Chat")
    st.markdown("Welcome to ShopEase! How can I help you today?")
    
    # Chat container
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        for message in st.session_state.messages:
            render_chat_message(
                role=message.get("role", "assistant"),
                content=message.get("content", ""),
                timestamp=message.get("timestamp")
            )
        
        # Show typing indicator if processing
        if st.session_state.is_typing:
            render_typing_indicator()
    
    # Input area
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create input form
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Your message:",
                placeholder="Ask about orders, returns, products...",
                label_visibility="collapsed"
            )
        
        with col2:
            submit_button = st.form_submit_button("Send", use_container_width=True, type="primary")
    
    # Handle form submission
    if submit_button and user_input.strip():
        # Add user message to history
        user_message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        }
        st.session_state.messages.append(user_message)
        
        # Show typing indicator
        st.session_state.is_typing = True
        
        # Get AI response
        response_container = st.empty()
        full_response = ""
        
        # Stream the response
        for token in send_message(user_input, st.session_state.session_id, stream=True):
            full_response += token
            response_container.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🛍️ ShopEase Assistant</strong>
                <div>{full_response}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Add assistant response to history
        if full_response:
            assistant_message = {
                "role": "assistant",
                "content": full_response,
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.messages.append(assistant_message)
        
        # Hide typing indicator and rerun
        st.session_state.is_typing = False
        st.rerun()


def main():
    """Main application entry point"""
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Render main chat interface
    render_chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>© 2024 ShopEase. All rights reserved.</p>
        <p>Need help? Contact us at support@shopease.com | 1-800-SHOP-EASE</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    import os
    main()