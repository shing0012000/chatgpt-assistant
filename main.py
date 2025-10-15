import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("=== Simple ChatGPT Assistant ===")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    # Send the user's message to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # you can change to 'gpt-3.5-turbo' if needed
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    # Print the AI’s reply
    reply = response.choices[0].message.content
    print(f"Assistant: {reply}\n")
