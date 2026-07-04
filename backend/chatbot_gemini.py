"""
Gemini Chatbot Implementation
Alternative to OpenAI using Google's Gemini API (free tier available)
"""

from typing import AsyncGenerator, Optional, Dict, List
import os
import time
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
import json
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests.exceptions

from utils.prompts import get_system_prompt, detect_intent
from utils.memory import memory_manager


class GeminiChatbotEngine:
    """
    Core chatbot engine using Google Gemini API with streaming support.
    """
    
    def __init__(self, model_name: str = "gemini-1.5-flash", temperature: float = 0.7, max_retries: int = 3):
        """
        Initialize the Gemini chatbot engine.
        
        Args:
            model_name: Gemini model to use (default: gemini-1.5-flash)
            temperature: Sampling temperature for response generation
            max_retries: Maximum number of retries for rate limit errors
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_retries = max_retries
        self.client = None
        self._initialize_client()
        self.last_request_time = 0
        self.min_request_interval = 4  # Minimum 4 seconds between requests (increased)
        self.request_count = 0
        self.rate_limit_window = 60  # 60 second window
        self.max_requests_per_window = 55  # Stay under 60 limit
    
    def _initialize_client(self):
        """Initialize the Gemini client."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        
        # Initialize LangChain Gemini client
        self.client = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            google_api_key=api_key,
            convert_system_message_to_human=True  # Gemini doesn't support system messages directly
        )
    
    def _build_messages(self, session_id: str, user_message: str) -> list:
        """
        Build the message list for the LLM including system prompt and history.
        Uses sliding window to keep only last 3-4 turns to reduce token load.
        
        Args:
            session_id: Chat session identifier
            user_message: Current user message
            
        Returns:
            List of messages for the LLM
        """
        messages = []
        
        # Get conversation history from memory
        memory_vars = memory_manager.get_memory_variables(session_id)
        chat_history = memory_vars.get("chat_history", [])
        
        # Sliding window: Keep only last 3-4 turns (6-8 messages)
        # Each turn = user message + assistant message
        max_turns = 3  # Keep last 3 turns (adjust as needed)
        max_messages = max_turns * 2  # 2 messages per turn
        
        if len(chat_history) > max_messages:
            # Keep only the most recent messages
            chat_history = chat_history[-max_messages:]
        
        # Add conversation history
        messages.extend(chat_history)
        
        # Add current user message
        messages.append(HumanMessage(content=user_message))
        
        return messages
    
    def _add_request_delay(self):
        """Add delay between requests to prevent rate limiting."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        # Enforce minimum delay between requests
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            print(f"⏳ Rate limit prevention: Waiting {sleep_time:.1f}s...")
            time.sleep(sleep_time)
        
        # Track request count for rate limiting
        self.request_count += 1
        self.last_request_time = time.time()
        
        # Log rate limit status
        if self.request_count % 10 == 0:
            print(f"📊 Request count: {self.request_count} in last {self.rate_limit_window}s")
    
    async def generate_response_stream(
        self, 
        session_id: str, 
        user_message: str
    ) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response from Gemini with retry logic.
        
        Args:
            session_id: Chat session identifier
            user_message: User's message
            
        Yields:
            Response tokens as they are generated
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # Add delay before request to prevent rate limiting
                self._add_request_delay()
                
                # Build messages
                messages = self._build_messages(session_id, user_message)
                
                # Get system prompt
                system_prompt = get_system_prompt()
                
                # For Gemini, we need to prepend system prompt to the first message
                if messages and isinstance(messages[0], HumanMessage):
                    messages[0] = HumanMessage(content=f"{system_prompt}\n\nUser: {messages[0].content}")
                
                # Generate response with streaming using astream
                full_response = ""
                async for chunk in self.client.astream(messages):
                    if hasattr(chunk, 'content') and chunk.content:
                        token = str(chunk.content)
                        full_response += token
                        yield token
                
                # Save the complete response to memory
                memory_manager.add_user_message(session_id, user_message)
                if isinstance(full_response, str):
                    memory_manager.add_ai_message(session_id, full_response)
                    memory_manager.save_memory(session_id)
                
                # Success - exit retry loop
                return
                
            except Exception as e:
                last_error = e
                error_msg = str(e).lower()
                
                # Check if it's a rate limit error
                if "quota" in error_msg or "rate" in error_msg or "limit" in error_msg:
                    if attempt < self.max_retries - 1:
                        # Calculate wait time with exponential backoff (longer delays)
                        wait_time = min(3 ** attempt, 60)  # 3s, 9s, 27s (more conservative)
                        yield f"\n\n⏳ **Rate limit hit. Waiting {wait_time} seconds before retry...**\n"
                        time.sleep(wait_time)
                    else:
                        # Final attempt failed - suggest waiting longer
                        yield (
                            "\n\n⚠️ **Rate Limit Exceeded**\n\n"
                            "I've reached the API rate limit. Please wait 60 seconds before trying again.\n\n"
                            "To avoid this in the future:\n"
                            "- Wait a few seconds between messages\n"
                            "- The system automatically spaces out requests\n\n"
                            "In the meantime:\n"
                            "- Check our FAQ section for quick answers\n"
                            "- Email us at support@shopease.com\n"
                            "- Call us at 1-800-SHOP-EASE\n\n"
                            "Thank you for your patience! 🙏"
                        )
                elif "connection" in error_msg or "reset" in error_msg or "timeout" in error_msg:
                    # Handle connection errors gracefully
                    yield (
                        "\n\n⚠️ **Connection Issue**\n\n"
                        "I'm having trouble connecting. Please try again in a moment.\n\n"
                        "If the issue persists, please contact our support team at:\n"
                        "- Email: support@shopease.com\n"
                        "- Phone: 1-800-SHOP-EASE"
                    )
                    break
                else:
                    # Other errors
                    yield (
                        "\n\n⚠️ **Service Temporarily Unavailable**\n\n"
                        "I'm experiencing technical difficulties. Please try again in a few moments.\n\n"
                        "If the issue persists, please contact our support team at:\n"
                        "- Email: support@shopease.com\n"
                        "- Phone: 1-800-SHOP-EASE"
                    )
                    break
    
    def generate_response(
        self, 
        session_id: str, 
        user_message: str
    ) -> tuple[str, Optional[str]]:
        """
        Generate a non-streaming response (fallback method) with retry logic.
        
        Args:
            session_id: Chat session identifier
            user_message: User's message
            
        Returns:
            Tuple of (response_text, error_message)
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # Add delay before request to prevent rate limiting
                self._add_request_delay()
                
                # Build messages
                messages = self._build_messages(session_id, user_message)
                
                # Get system prompt
                system_prompt = get_system_prompt()
                
                # For Gemini, prepend system prompt to first message
                if messages and isinstance(messages[0], HumanMessage):
                    messages[0] = HumanMessage(content=f"{system_prompt}\n\nUser: {messages[0].content}")
                
                # Generate response
                response = self.client.invoke(messages)
                response_text = str(response.content) if hasattr(response, 'content') else str(response)
                
                # Save to memory
                memory_manager.add_user_message(session_id, user_message)
                memory_manager.add_ai_message(session_id, response_text)
                memory_manager.save_memory(session_id)
                
                return response_text, None
                
            except Exception as e:
                last_error = e
                error_msg = str(e).lower()
                
                if "quota" in error_msg or "rate" in error_msg or "limit" in error_msg:
                    if attempt < self.max_retries - 1:
                        wait_time = min(2 ** attempt, 60)
                        time.sleep(wait_time)
                    else:
                        error_msg = (
                            "⚠️ **Rate Limit Exceeded**\n\n"
                            "I'm experiencing high traffic at the moment. Please wait a minute and try again. "
                            "Thank you for your patience! 🙏"
                        )
                        return error_msg, "rate_limit"
                elif "connection" in error_msg or "reset" in error_msg or "timeout" in error_msg:
                    error_msg = (
                        "⚠️ **Connection Issue**\n\n"
                        "I'm having trouble connecting. Please try again in a moment.\n\n"
                        "If the issue persists, contact us at:\n"
                        "- Email: support@shopease.com\n"
                        "- Phone: 1-800-SHOP-EASE"
                    )
                    return error_msg, "connection_error"
                else:
                    error_msg = (
                        "⚠️ **Service Temporarily Unavailable**\n\n"
                        "I'm experiencing technical difficulties. Please try again in a few moments.\n\n"
                        "If the issue persists, contact us at:\n"
                        "- Email: support@shopease.com\n"
                        "- Phone: 1-800-SHOP-EASE"
                    )
                    return error_msg, "api_error"
        
        # If we exhausted all retries
        error_msg = (
            "⚠️ **Service Busy**\n\n"
            "I'm currently experiencing high demand. Please try again in a moment.\n\n"
            "Thank you for your patience! 🙏"
        )
        return error_msg, "rate_limit"
    
    def get_conversation_history(self, session_id: str) -> list:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Chat session identifier
            
        Returns:
            List of messages in the conversation
        """
        return memory_manager.get_chat_history(session_id)
    
    def clear_conversation(self, session_id: str) -> bool:
        """
        Clear conversation history for a session.
        
        Args:
            session_id: Chat session identifier
            
        Returns:
            True if cleared successfully
        """
        return memory_manager.clear_session(session_id)


# Global Gemini chatbot engine instance
gemini_chatbot_engine = GeminiChatbotEngine()