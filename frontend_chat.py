import os
import json
import argparse
from dotenv import load_dotenv
from vera_memory_system import VeraConsciousness
from datetime import datetime

load_dotenv()

import anthropic
from openai import OpenAI, RateLimitError

# Setup
vera = VeraConsciousness()

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("--provider", choices=["openai", "claude"], required=True)
args = parser.parse_args()
provider = args.provider

# Load API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Init
chat_history = []
timestamp_label = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, f"chat-{timestamp_label}_{provider}.json")

print("👤 You may begin chatting. Type 'exit' to quit or '/reset' to clear history.\n")

while True:
    user_input = input("You: ")

    # 🧼 Skip blank inputs
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

    print(f"Vera: {reply}\n")
    chat_history.append({"role": "assistant", "content": reply})
    vera.store_interaction(chat_history[-2:], authenticity_level="high")
