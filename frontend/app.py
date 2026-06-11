import streamlit as st
import requests
import uuid
import os
import sys

# Add the parent directory to the path so we can import core.config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.config import settings

# --- Page Configuration ---
st.set_page_config(
    page_title=settings.PROJECT_NAME,
    page_icon="💖",
    layout="centered"
)

# --- CSS Styling for Premium Look ---
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex;
    }
    .chat-message.user {
        background-color: #2b313e;
        border: 1px solid #4a5568;
    }
    .chat-message.bot {
        background-color: #1a202c;
        border: 1px solid #2d3748;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .avatar img {
        max-width: 50px;
        max-height: 50px;
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .message {
        width: 80%;
        padding: 0 1.5rem;
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI Header ---
st.title(f"Chat with {settings.GF_NAME} 💖")
st.markdown("---")

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input ---
if prompt := st.chat_input("Type your message here..."):
    # Append user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # API Request to FastAPI Backend
    api_url = f"http://localhost:{settings.API_PORT}/chat_stream"
    payload = {
        "user_id": st.session_state.user_id,
        "message": prompt
    }

    with st.chat_message("assistant"):
        try:
            response = requests.post(api_url, json=payload, stream=True)
            response.raise_for_status()
            
            # Generator to yield chunks from the stream
            def generate():
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        yield chunk
            
            # Use st.write_stream to type out the response
            full_response = st.write_stream(generate())
            
        except Exception as e:
            full_response = f"Sorry, I'm having trouble connecting to my brain right now... (Error: {e})"
            st.markdown(full_response)

    # Append bot message to state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
