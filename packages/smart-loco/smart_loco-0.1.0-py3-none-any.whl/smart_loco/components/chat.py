import streamlit as st
from smart_loco.client.llm import call_llm_chat_local, get_local_models
import json
import os
from datetime import datetime

CHAT_HISTORY_FILE = os.path.expanduser("~/.smart_loco/chat/history.json")


def load_chat_history():
    """Load chat history from local storage"""
    try:
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(CHAT_HISTORY_FILE), exist_ok=True)
        
        if os.path.exists(CHAT_HISTORY_FILE):
            with open(CHAT_HISTORY_FILE, 'r') as f:
                history = json.load(f)
                if not st.session_state.chat_history:
                    st.session_state.chat_history = history
    except Exception as e:
        st.error(f"Error loading chat history: {str(e)}")


def save_chat_history():
    """Save chat history to local storage"""
    try:
        with open(CHAT_HISTORY_FILE, 'w') as f:
            json.dump(st.session_state.chat_history, f)
    except Exception as e:
        st.error(f"Error saving chat history: {str(e)}")


def clear_chat_history():
    """Clear chat history from session and local storage"""
    try:
        st.session_state.chat_history = []
        if os.path.exists(CHAT_HISTORY_FILE):
            os.remove(CHAT_HISTORY_FILE)
        st.success("Chat history cleared!")
    except Exception as e:
        st.error(f"Error clearing chat history: {str(e)}")


def add_message(role: str, content: str):
    """Add a message to the chat history"""
    st.session_state.chat_history.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    save_chat_history()


def display_chat_history():
    """Display chat history in the UI"""
    for message in st.session_state.chat_history:
        role = message["role"]
        with st.chat_message(role):
            st.write(message["content"])
            # Show timestamp in small, light gray text
            st.caption(f"Sent at {datetime.fromisoformat(message['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")


def show():
    # Get available local models
    local_models = get_local_models()
    if not local_models:
        st.sidebar.error("No local models available. Please check your local model setup.")
        return
    
    # Model selection in sidebar
    model = st.sidebar.selectbox(
        "Select Model",
        local_models
    )

    # Create a sidebar for settings
    with st.sidebar:
        st.write("### Chat Settings")
        
        # System prompt handling...
        if 'system_prompt' not in st.session_state:
            st.session_state.system_prompt = "You are a helpful AI assistant."

        system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.system_prompt,
            help="Set the behavior and context for the AI",
            height=100
        )
        st.session_state.system_prompt = system_prompt

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="Higher values make the output more random, lower values make it more focused"
        )

        if st.button("Clear History", use_container_width=True):
            clear_chat_history()
            st.rerun()

    # Rest of the chat interface...
    load_chat_history()
    display_chat_history()

    if prompt := st.chat_input("Type your message here..."):
        add_message("user", prompt)
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                for chunk in call_llm_chat_local(
                    model=model,
                    temperature=temperature,
                    system_prompt=st.session_state.system_prompt,
                    user_prompt=prompt,
                    stream=True
                ):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                add_message("assistant", full_response)

            except Exception as e:
                error_message = f"Error getting response: {str(e)}"
                st.error(error_message)
                add_message("system", error_message) 