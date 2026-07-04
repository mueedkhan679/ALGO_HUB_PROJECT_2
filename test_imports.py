"""
Test script to verify all imports work correctly
Run this before starting the application
"""

import sys

def test_imports():
    """Test all critical imports"""
    print("Testing imports...\n")
    
    errors = []
    
    # Test backend imports
    print("1. Testing backend imports...")
    try:
        from fastapi import FastAPI
        print("   ✓ FastAPI")
    except ImportError as e:
        errors.append(f"FastAPI: {e}")
        print(f"   ✗ FastAPI: {e}")
    
    try:
        from langchain_openai import ChatOpenAI
        print("   ✓ LangChain OpenAI")
    except ImportError as e:
        errors.append(f"LangChain OpenAI: {e}")
        print(f"   ✗ LangChain OpenAI: {e}")
    
    try:
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
        print("   ✓ LangChain Messages")
    except ImportError as e:
        errors.append(f"LangChain Messages: {e}")
        print(f"   ✗ LangChain Messages: {e}")
    
    try:
        from langchain_core.callbacks.base import BaseCallbackHandler
        print("   ✓ LangChain Callbacks")
    except ImportError as e:
        errors.append(f"LangChain Callbacks: {e}")
        print(f"   ✗ LangChain Callbacks: {e}")
    
    try:
        from langchain_community.chat_message_histories import ChatMessageHistory
        print("   ✓ LangChain ChatMessageHistory")
    except ImportError as e:
        errors.append(f"LangChain ChatMessageHistory: {e}")
        print(f"   ✗ LangChain ChatMessageHistory: {e}")
    
    # Test frontend imports
    print("\n2. Testing frontend imports...")
    try:
        import streamlit as st
        print("   ✓ Streamlit")
    except ImportError as e:
        errors.append(f"Streamlit: {e}")
        print(f"   ✗ Streamlit: {e}")
    
    try:
        import requests
        print("   ✓ Requests")
    except ImportError as e:
        errors.append(f"Requests: {e}")
        print(f"   ✗ Requests: {e}")
    
    # Test utils imports
    print("\n3. Testing utils imports...")
    try:
        from utils.memory import MemoryManager
        print("   ✓ Memory Manager")
    except ImportError as e:
        errors.append(f"Memory Manager: {e}")
        print(f"   ✗ Memory Manager: {e}")
    
    try:
        from utils.prompts import get_system_prompt, detect_intent
        print("   ✓ Prompts")
    except ImportError as e:
        errors.append(f"Prompts: {e}")
        print(f"   ✗ Prompts: {e}")
    
    # Summary
    print("\n" + "="*50)
    if errors:
        print(f"❌ Found {len(errors)} import error(s):")
        for error in errors:
            print(f"   - {error}")
        print("\nPlease install missing dependencies:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("✅ All imports successful!")
        print("\nYou can now run the application:")
        print("   1. Backend: uvicorn backend.main:app --reload --port 8000")
        print("   2. Frontend: streamlit run frontend/app.py")
        return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)