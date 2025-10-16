import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()
# For Streamlit Cloud, it will read from secrets automatically
api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets["OPENROUTER_API_KEY"]

st.set_page_config(page_title="ChatGPT Assistant (Free API)", page_icon="💬")
st.title("💬 Simple ChatGPT Assistant (via OpenRouter)")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a helpful assistant."}]

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Streamlit Assistant Demo",
    }

    payload = {
        "model": "gpt-3.5-turbo",  # or try 'mistralai/mixtral-8x7b'
        "messages": st.session_state["messages"],
    }

response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    if "choices" in data and len(data["choices"]) > 0:
        reply = data["choices"][0]["message"]["content"]
        st.session_state["messages"].append({"role": "assistant", "content": reply})
    else:
        st.error("⚠️ The model returned an unexpected response format.")
else:
    st.error(f"⚠️ API Error {response.status_code}: {response.text}")


for message in st.session_state["messages"][1:]:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])
