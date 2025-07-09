# /scripts/frontend_chat.py

import os
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv

import anthropic
from openai import OpenAI, RateLimitError
from vera_memory_system import VeraConsciousness

# Load environment variables
load_dotenv()

# CLI argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--provider", choices=["openai", "claude"], required=True)
parser.add_argument("--user", required=False, help="Override USER_ID (Mem0 context)")
args = parser.parse_args()

# Load context identifiers
env_user = os.getenv("USER_ID")
personality = os.getenv("PERSONALITY", "vera")
role = os.getenv("ROLE", "consultation")

user_id = args.user or env_user
full_name = f"{user_id}_{personality}_{role}"

# Initialize Vera memory system
vera = VeraConsciousness(user_id=user_id)

# Load API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Chat session setup
chat_history = []
timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, f"chat-{timestamp}_{provider}_{full_name}.json")

print(f"👤 You may begin chatting with: {full_name}")
print("💬 Type 'exit' to quit or '/reset' to clear history.\n")

while True:
    user_input = input("You: ")

    if not user_input.strip():
        print("⚠️ Empty input ignored.")
        continue

    if user_input.lower() in ["exit", "quit"]:
        print("👋 Ending chat. Saving log...")
        with open(log_path, "w") as f:
            json.dump(chat_history, f, indent=2)
        print(f"📝 Log saved to: {log_path}")
        break

    if user_input.lower() == "/reset":
        chat_history.clear()
        print("🔄 Chat history cleared.")
        continue

    chat_history.append({"role": "user", "content": user_input})

    try:
        if provider == "openai":
            client = OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=chat_history
            )
            reply = response.choices[0].message.content

        elif provider == "claude":
            client = anthropic.Anthropic(api_key=anthropic_api_key)
            response = client.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=1024,
                temperature=0.7,
                messages=chat_history
            )
            reply = response.content[0].text

    except RateLimitError:
        print("⚠️ OpenAI quota exceeded or rate limited.")
        reply = "[OpenAI quota exceeded.]"
        if provider == "openai":
            print("💡 Tip: Try again later or use --provider claude")
            continue

    except Exception as e:
        print(f"❌ Error: {e}")
        reply = "[Error generating response.]"
        continue

    print(f"{personality.capitalize()}: {reply}\n")
    chat_history.append({"role": "assistant", "content": reply})
    vera.store_interaction(chat_history[-2:], authenticity_level="high")
