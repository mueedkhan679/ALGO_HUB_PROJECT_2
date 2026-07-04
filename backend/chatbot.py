from typing import AsyncGenerator, Optional, Dict
import os
import time
from openai import RateLimitError, APIError
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json
from datetime import datetime

from utils.prompts import get_system_prompt, detect_intent
from utils.memory import memory_manager




class ChatbotEngine:
    """
    Core chatbot engine that handles LLM interactions with streaming support.
    """
    
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.7, max_retries: int = 3):
        """
        Initialize the chatbot engine.
        
        Args:
            model_name: OpenAI model to use (default: gpt-4o)
            temperature: Sampling temperature for response generation
            max_retries: Maximum number of retries for rate limit errors
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_retries = max_retries
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.client = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            openai_api_key=api_key,
            streaming=True
        )
    
    def _build_messages(self, session_id: str, user_message: str) -> list:
        """
        Build the message list for the LLM including system prompt and history.
        
        Args:
            session_id: Chat session identifier
            user_message: Current user message
            
        Returns:
            List of messages for the LLM
        """
        messages = []
        
        # Add system message
        system_prompt = get_system_prompt()
        messages.append(SystemMessage(content=system_prompt))
        
        # Get conversation history from memory
        memory_vars = memory_manager.get_memory_variables(session_id)
        chat_history = memory_vars.get("chat_history", [])
        
        # Add conversation history (already in correct format)
        messages.extend(chat_history)
        
        # Add current user message
        messages.append(HumanMessage(content=user_message))
        
        return messages
    
    async def generate_response_stream(
        self, 
        session_id: str, 
        user_message: str
    ) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response from the LLM with retry logic.
        
        Args:
            session_id: Chat session identifier
            user_message: User's message
            
        Yields:
            Response tokens as they are generated
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # Build messages
                messages = self._build_messages(session_id, user_message)
                
                # Generate response with streaming using astream
                full_response = ""
                async for chunk in self.client.astream(messages):
                    if hasattr(chunk, 'content'):
                        token = chunk.content
                        if token:
                            full_response += token
                            yield token
                
                # Save the complete response to memory
                memory_manager.add_user_message(session_id, user_message)
                memory_manager.add_ai_message(session_id, full_response)
                memory_manager.save_memory(session_id)
                
                # Success - exit retry loop
                return
                
            except RateLimitError as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    # Calculate wait time with exponential backoff
                    wait_time = min(2 ** attempt, 60)  # Cap at 60 seconds
                    yield f"\n\n⏳ **Rate limit hit. Retrying in {wait_time} seconds...**\n"
                    time.sleep(wait_time)
                else:
                    # Final attempt failed - show user-friendly message
                    yield (
                        "\n\n⚠️ **Rate Limit Exceeded**\n\n"
                        "I'm experiencing high traffic at the moment. Please wait a minute and try again. "
                        "Our team has been notified and we're working to resolve this.\n\n"
                        "In the meantime, you can:\n"
                        "- Check our FAQ section for quick answers\n"
                        "- Email us at support@shopease.com\n"
                        "- Call us at 1-800-SHOP-EASE\n\n"
                        "Thank you for your patience! 🙏"
                    )
                    
            except APIError as e:
                last_error = e
                yield (
                    "\n\n⚠️ **Service Temporarily Unavailable**\n\n"
                    "I'm experiencing technical difficulties connecting to our AI service. "
                    "Please try again in a few moments.\n\n"
                    "If the issue persists, please contact our support team at:\n"
                    "- Email: support@shopease.com\n"
                    "- Phone: 1-800-SHOP-EASE"
                )
                # Don't retry on API errors
                break
                
            except Exception as e:
                last_error = e
                yield (
                    "\n\n⚠️ **Unexpected Error**\n\n"
                    "Something went wrong while processing your request. "
                    "Please try again or contact our support team for assistance.\n\n"
                    "We apologize for the inconvenience!"
                )
                # Don't retry on unknown errors
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
                # Build messages
                messages = self._build_messages(session_id, user_message)
                
                # Generate response
                response = self.client.invoke(messages)
                response_text = response.content
                
                # Save to memory
                memory_manager.add_user_message(session_id, user_message)
                memory_manager.add_ai_message(session_id, response_text)
                memory_manager.save_memory(session_id)
                
                return response_text, None
                
            except RateLimitError:
                last_error = "rate_limit"
                if attempt < self.max_retries - 1:
                    # Wait with exponential backoff before retrying
                    wait_time = min(2 ** attempt, 60)
                    time.sleep(wait_time)
                else:
                    error_msg = (
                        "⚠️ **Rate Limit Exceeded**\n\n"
                        "I'm experiencing high traffic at the moment. Please wait a minute and try again. "
                        "Thank you for your patience! 🙏"
                    )
                    return error_msg, "rate_limit"
            
            except APIError:
                error_msg = (
                    "⚠️ **Service Temporarily Unavailable**\n\n"
                    "I'm experiencing technical difficulties. Please try again in a few moments.\n\n"
                    "If the issue persists, contact us at:\n"
                    "- Email: support@shopease.com\n"
                    "- Phone: 1-800-SHOP-EASE"
                )
                return error_msg, "api_error"
            
            except Exception as e:
                error_msg = (
                    "⚠️ **Unexpected Error**\n\n"
                    "Something went wrong. Please try again or contact our support team.\n\n"
                    "We apologize for the inconvenience!"
                )
                return error_msg, "unknown_error"
        
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


# Global chatbot engine instance
chatbot_engine = ChatbotEngine()