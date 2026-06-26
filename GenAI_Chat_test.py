import streamlit as st
from google import genai
import json
from google.genai import types

HISTORY_FILE = "chat_history.json"

# Load history from JSON file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# Save history to JSON file
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)


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
    # Initialize session state with loaded history
    st.session_state.messages = load_history()

st.title("🐍 Python Expert Chatbot")
st.markdown("<h1 style='color: black; font-size: 40px;'>PYTHON AI ASSISTANT</h1><p style='color: blue; font-size: 20px;'>Python AI Assistant can help to your questions related to python</p>", unsafe_allow_html=True)


    

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

    # Persist to disk
    save_history(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
