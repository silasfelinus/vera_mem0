#!/bin/bash

set -e  # Stop on any error

echo "🧠 Welcome to Vera Memory System setup!"

# Step 0: Git update
if command -v git >/dev/null 2>&1; then
  echo "🔄 Checking for updates from Git..."
  git pull origin main || echo "⚠️ Git pull failed (not a git repo or no access)"
else
  echo "⚠️ Git is not installed or not in PATH. Skipping update."
fi

# Step 1: Copy .env_example → .env if not already done
if [ ! -f .env ]; then
  cp .env_example .env
  echo "✓ Created .env from .env_example"
else
  echo "🔁 .env already exists – skipping copy"
fi

# Step 2: Prompt user to edit .env
echo ""
echo "⚠️  IMPORTANT: Please edit the .env file to add your MEM0_API_KEY and USER_ID."
echo "   You can open it with any editor (e.g., nano .env or code .env)"
echo ""
read -p "✅ Press Enter when you've finished editing .env..."

# Step 3: Create venv if not exists
if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "✓ Created Python virtual environment"
fi

# Step 4: Activate venv and install requirements
source venv/bin/activate
echo "📦 Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 5: Run the program
echo ""
echo "🚀 Running vera_memory_system.py..."
python vera_memory_system.py
