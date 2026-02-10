import streamlit as st
import json
import os
import urllib.request

# Page config
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

st.title("🤖 Simple Gemini Chatbot")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found in environment variables.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
prompt = st.chat_input("Ask something...")

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Gemini API request
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-pro:generateContent?key=" + API_KEY
    )

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        reply = f"Error: {e}"

    # Show assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
