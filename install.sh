#!/bin/bash

set -e  # Stop on any error

echo "🧠 Welcome to the Vera Memory System setup!"

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

# Step 2: Prompt user to enter MEM0 key and USER_ID
echo ""
echo "⚠️  IMPORTANT: Please edit the .env file to include your MEM0_API_KEY and USER_ID."
echo ""
read -p "Do you want to set a custom USER_ID now? (y/n) " confirm
if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
  read -p "Enter a USER_ID (e.g., vera_alice_consultation): " custom_user
  if grep -q "^USER_ID=" .env; then
    sed -i.bak "s/^USER_ID=.*/USER_ID=$custom_user/" .env
  else
    echo "USER_ID=$custom_user" >> .env
  fi
  echo "✓ Set USER_ID to $custom_user"
else
  echo "ℹ️ Using USER_ID already defined in .env"
fi

echo ""
echo "You can open .env with any editor (e.g., nano .env or code .env)"
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

# Step 5: Run the core memory system
source .env
echo ""
echo "🚀 Running core memory system for: $USER_ID"
python scripts/vera_memory_system.py "$USER_ID"

# Step 6: Load personality training files
echo ""
echo "🧠 Uploading training files for: $USER_ID"
python scripts/load_personality.py --user "$USER_ID"

# Step 7: Generate wake-up context
echo ""
echo "🪬 Generating wake-up context for: $USER_ID"
python scripts/vera_wake_up_bridge.py --user "$USER_ID"
