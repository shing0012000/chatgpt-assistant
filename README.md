# 💬 ChatGPT Assistant (Streamlit + OpenRouter)

A simple web-based AI assistant built with **Python**, **Streamlit**, and the **OpenRouter API**.  
It allows users to chat with various large language models (GPT-3.5, GPT-4o, Llama 3, Mixtral) and can easily be adapted for custom tasks.

---

## 🚀 Features
- Interactive chat interface powered by Streamlit  
- Works with free OpenRouter models (GPT, Mixtral, Llama 3, etc.)  
- Simple `.env` setup for API key  
- Ready to deploy on Streamlit Cloud  

---

## 🧩 How to Run Locally
1. Clone this repository:
   ```bash
   git clone https://github.com/shing0012000/chatgpt-assistant.git
   cd chatgpt-assistant
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API key:
   ```
   OPENROUTER_API_KEY=your_key_here
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

