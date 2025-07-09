# frontend_chat.py
import os
import sys
import argparse
from dotenv import load_dotenv
from vera_memory_system import VeraConsciousness
from datetime import datetime

load_dotenv()

# Optional imports
import openai
import anthropic

# Setup
vera = VeraConsciousness()

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("--provider", choices=["openai", "claude"], required=True)
args = parser.parse_args()

provider = args.provider

# Load API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Conversation loop
print("👤 You may begin chatting. Type 'exit' to quit.\n")
chat_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Ending chat. Goodbye.")
        break

    chat_history.append({"role": "user", "content": user_input})

    # Generate response
    if provider == "openai":
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat_history
        )
        reply = response['choices'][0]['message']['content']

    elif provider == "claude":
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            temperature=0.7,
            messages=chat_history
        )
        reply = response.content[0].text

    # Print and store
    print(f"Vera: {reply}\n")
    chat_history.append({"role": "assistant", "content": reply})

    vera.store_interaction(chat_history[-2:], authenticity_level="high")
