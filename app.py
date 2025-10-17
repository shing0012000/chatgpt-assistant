import os
import streamlit as st
import requests
from dotenv import load_dotenv
import json

# -----------------------------------------
# 🧩 Page Setup
# -----------------------------------------
st.set_page_config(page_title="AI Assistant (OpenRouter + Web Search)", page_icon="🌐")
st.title("AI Assistant with Web Search 🌐")

load_dotenv()  # For local dev, Streamlit Cloud uses st.secrets automatically

# Load API keys
OPENROUTER_KEY = (
    os.getenv("OPENROUTER_API_KEY")
    or st.secrets["api_keys"].get("openrouter")
)
SERPER_KEY = (
    os.getenv("SERPER_API_KEY")
    or st.secrets["api_keys"].get("serper")
)

# -----------------------------------------
# 🧠 Mode selection
# -----------------------------------------
mode = st.radio("Choose mode:", ["💬 Chat", "🌍 Chat with Web Search"])

# -----------------------------------------
# 🌍 MODE 1: Web Search + ChatGPT
# -----------------------------------------
if mode == "🌍 Chat with Web Search":
    query = st.text_input("Ask me anything:")
    num_results = st.slider("Number of search results", 3, 10, 5)

    if st.button("Search and Answer") and query:
        # Step 1: Perform web search via Serper.dev
        search_url = "https://google.serper.dev/search"
        payload = {"q": query, "num": num_results}
        headers = {
            "X-API-KEY": SERPER_KEY,
            "Content-Type": "application/json",
        }
        search_results = requests.post(search_url, headers=headers, json=payload).json()

        # Extract snippets
        snippets = []
        for item in search_results.get("organic", []):
            snippets.append(f"- {item.get('title')}: {item.get('snippet')}")
        context = "\n".join(snippets)

        # Step 2: Send combined query + context to OpenRouter
        openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
        }

        prompt = f"Use the following web search results to answer the question.\n{context}\n\nQuestion: {query}"

        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant with access to web search results."},
                {"role": "user", "content": prompt},
            ],
        }

        response = requests.post(openrouter_url, headers=headers, json=data)
        answer = response.json()["choices"][0]["message"]["content"]

        st.subheader("Answer:")
        st.write(answer)

        with st.expander("Web Sources"):
            st.write(context)

# -----------------------------------------
# 💬 MODE 2: Normal Chat (no web search)
# -----------------------------------------
elif mode == "💬 Chat":
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})

        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Streamlit Assistant Demo",
        }

        payload = {
            "model": "gpt-4o-mini",  # You can also use 'mistralai/mixtral-8x7b'
            "messages": st.session_state["messages"],
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                reply = data["choices"][0]["message"]["content"]
                st.session_state["messages"].append({"role": "assistant", "content": reply})
            else:
                st.error("⚠️ Unexpected response format.")
        else:
            st.error(f"⚠️ API Error {response.status_code}: {response.text}")

    # Display conversation
    for message in st.session_state["messages"][1:]:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])
