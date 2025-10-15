import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit page setup
st.set_page_config(page_title="ChatGPT Assistant", page_icon="💬")
st.title("💬 Simple ChatGPT Assistant")
st.write("Ask me anything!")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# User input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user's message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Get response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # use "gpt-3.5-turbo" if you prefer
        messages=st.session_state["messages"]
    )

    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})

# Display chat history
for message in st.session_state["messages"][1:]:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])
