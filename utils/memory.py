"""
Memory Management Module
Handles conversation history using LangChain's ConversationBufferMemory
"""

from typing import Dict, Optional, List
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
import json
import os
from datetime import datetime

class MemoryManager:
    """
    Manages conversation memory for multiple chat sessions.
    Uses LangChain's ChatMessageHistory for storing chat history.
    """
    
    def __init__(self, storage_dir: str = "memory_storage"):
        """
        Initialize the MemoryManager.
        
        Args:
            storage_dir: Directory to store memory files
        """
        self.storage_dir = storage_dir
        self.sessions: Dict[str, ChatMessageHistory] = {}
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
    
    def get_or_create_session(self, session_id: str) -> ChatMessageHistory:
        """
        Get an existing session or create a new one.
        
        Args:
            session_id: Unique identifier for the chat session
            
        Returns:
            ChatMessageHistory instance for the session
        """
        if session_id not in self.sessions:
            # Try to load existing memory from file
            memory = self._load_memory(session_id)
            if memory is None:
                # Create new memory if no saved session exists
                memory = ChatMessageHistory()
            self.sessions[session_id] = memory
        
        return self.sessions[session_id]
    
    def _load_memory(self, session_id: str) -> Optional[ChatMessageHistory]:
        """
        Load memory from persistent storage.
        
        Args:
            session_id: Unique identifier for the chat session
            
        Returns:
            ChatMessageHistory instance or None if not found
        """
        file_path = os.path.join(self.storage_dir, f"{session_id}.json")
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            memory = ChatMessageHistory()
            
            # Reconstruct chat history from saved data
            for message in data.get("messages", []):
                if message["role"] == "user":
                    memory.add_message(HumanMessage(content=message["content"]))
                elif message["role"] == "assistant":
                    memory.add_message(AIMessage(content=message["content"]))
            
            return memory
        except Exception as e:
            print(f"Error loading memory for session {session_id}: {e}")
            return None
    
    def save_memory(self, session_id: str) -> bool:
        """
        Save memory to persistent storage.
        
        Args:
            session_id: Unique identifier for the chat session
            
        Returns:
            True if saved successfully, False otherwise
        """
        if session_id not in self.sessions:
            return False
        
        file_path = os.path.join(self.storage_dir, f"{session_id}.json")
        
        try:
            memory = self.sessions[session_id]
            messages = []
            
            # Extract messages from memory
            for message in memory.messages:
                if isinstance(message, HumanMessage):
                    messages.append({
                        "role": "user",
                        "content": message.content,
                        "timestamp": datetime.now().isoformat()
                    })
                elif isinstance(message, AIMessage):
                    messages.append({
                        "role": "assistant",
                        "content": message.content,
                        "timestamp": datetime.now().isoformat()
                    })
            
            data = {
                "session_id": session_id,
                "messages": messages,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving memory for session {session_id}: {e}")
            return False
    
    def clear_session(self, session_id: str) -> bool:
        """
        Clear a specific session's memory.
        
        Args:
            session_id: Unique identifier for the chat session
            
        Returns:
            True if cleared successfully, False otherwise
        """
        # Remove from active sessions
        if session_id in self.sessions:
            del self.sessions[session_id]
        
        # Remove from storage
        file_path = os.path.join(self.storage_dir, f"{session_id}.json")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception as e:
                print(f"Error clearing session {session_id}: {e}")
                return False
        return True
    
    def get_chat_history(self, session_id: str) -> list:
        """
        Get formatted chat history for a session.
        
        Args:
            session_id: Unique identifier for the chat session
            
        Returns:
            List of formatted message dictionaries
        """
        if session_id not in self.sessions:
            return []
        
        memory = self.sessions[session_id]
        messages = []
        
        for message in memory.messages:
            if isinstance(message, HumanMessage):
                messages.append({
                    "role": "user",
                    "content": message.content
                })
            elif isinstance(message, AIMessage):
                messages.append({
                    "role": "assistant",
                    "content": message.content
                })
        
        return messages
    
    def add_user_message(self, session_id: str, message: str):
        """
        Add a user message to the session memory.
        
        Args:
            session_id: Unique identifier for the chat session
            message: User's message content
        """
        memory = self.get_or_create_session(session_id)
        memory.add_message(HumanMessage(content=message))
    
    def add_ai_message(self, session_id: str, message: str):
        """
        Add an AI response to the session memory.
        
        Args:
            session_id: Unique identifier for the chat session
            message: AI's response content
        """
        memory = self.get_or_create_session(session_id)
        memory.add_message(AIMessage(content=message))
    
    def get_memory_variables(self, session_id: str) -> Dict:
        """
        Get memory variables for LangChain chain.
        
        Args:
            session_id: Unique identifier for the chat session
            
        Returns:
            Dictionary with memory variables
        """
        memory = self.get_or_create_session(session_id)
        return {"chat_history": memory.messages}


# Global memory manager instance
memory_manager = MemoryManager()