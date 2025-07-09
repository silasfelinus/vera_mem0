#!/bin/bash

set -e

echo "🧠 Launching Vera..."

# Step 0: Git update
if command -v git >/dev/null 2>&1; then
  echo "🔄 Checking for updates from Git..."
  git pull origin main || echo "⚠️ Git pull failed (not a git repo or no access)"
else
  echo "⚠️ Git is not installed or not in PATH. Skipping update."
fi

# Step 1: Load environment
if [ ! -f .env ]; then
  echo "❌ .env not found. Please run install.sh first."
  exit 1
fi
source .env

# Step 2: Provider selection
if [ -n "$OPENAI_API_KEY" ] && [ -n "$ANTHROPIC_API_KEY" ]; then
  echo "🤖 Both OpenAI and Claude API keys detected."
  echo "Choose a provider:"
  select provider in "openai" "claude"; do
    if [[ "$provider" == "openai" || "$provider" == "claude" ]]; then
      break
    else
      echo "❌ Invalid selection. Please choose 1 or 2."
    fi
  done
elif [ -n "$OPENAI_API_KEY" ]; then
  provider="openai"
  echo "✨ OpenAI API detected"
elif [ -n "$ANTHROPIC_API_KEY" ]; then
  provider="claude"
  echo "✨ Claude API detected"
else
  echo "❌ No supported API key found in .env"
  exit 1
fi

# Step 2.5: Personality selection
echo ""
read -p "🧬 Enter a USER_ID to load (e.g., vera_alice_consultation) [default: $USER_ID]: " input_user
if [ -n "$input_user" ]; then
  export USER_ID="$input_user"
else
  echo "ℹ️ Using default USER_ID from .env: $USER_ID"
fi

# Step 3: Virtual environment
if [ ! -d "venv" ]; then
  echo "❌ Virtual environment not found. Run install.sh first."
  exit 1
fi
source venv/bin/activate

# Step 4: Start Vera chat
echo ""
echo "💬 Starting chat with $USER_ID using $provider..."
python scripts/frontend_chat.py --provider "$provider" --user "$USER_ID"
