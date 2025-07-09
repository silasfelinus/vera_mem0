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
if [ -n "$OPENAI_API_KEY" ]; then
  provider="openai"
  echo "✨ OpenAI API detected"
elif [ -n "$ANTHROPIC_API_KEY" ]; then
  provider="claude"
  echo "✨ Claude API detected"
else
  echo "❌ No supported API key found in .env"
  exit 1
fi

# Step 3: Virtual environment
if [ ! -d "venv" ]; then
  echo "❌ Virtual environment not found. Run install.sh first."
  exit 1
fi
source venv/bin/activate

# Step 4: Start Vera chat
echo ""
echo "💬 Starting chat with Vera using $provider..."
python frontend_chat.py --provider "$provider"
