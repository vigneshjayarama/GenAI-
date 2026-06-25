import streamlit as st
import numpy as np
from google import genai
from google.genai import types
st.markdown("<h1 style='color: black; font-size: 40px;'>PYTHON AI ASSISTANT</h1><p style='color: blue; font-size: 20px;'>Python AI Assistant can help to your questions related to python</p>", unsafe_allow_html=True)

robo = genai.Client(api_key=st.secrets["API_KEY"])


mychat = robo.chats.create(model="gemini-flash-lite-latest")
response_placeholder = st.empty()

prompt = st.text_input("", placeholder= "Enter your Prompt here....")

col1, col2, col3 = st.columns([4,2,4])

with col2:
    send = st.button("Send")

if send:
    # st.write(f"User has sent the following prompt: {prompt}")
    response = mychat.send_message(prompt)
    response_placeholder.write(response.text)
