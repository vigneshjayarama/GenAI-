import streamlit as st
from google import genai
from google.genai import types

# Initialize everything once and keep alive in session state
if "mychat" not in st.session_state:
    st.session_state.robo = genai.Client(api_key=st.secrets["API_KEY"])
    
    config = types.GenerateContentConfig(
        system_instruction=(
            "You are an expert Python developer."
            " Answer only questions related to Python programming."
            " For any non-Python question, reply exactly:"
            " Please ask a Python-related question."
            " Do not answer questions outside the Python domain."
        )
    )
    st.session_state.mychat = st.session_state.robo.chats.create(
        model="gemini-flash-lite-latest", config=config
    )
    st.session_state.messages = []

st.title("🐍 Python Expert Chatbot")

# Display all previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle new input
prompt = st.chat_input("Ask a Python question...")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = st.session_state.mychat.send_message(prompt)
    
    with st.chat_message("assistant"):
        st.write(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
