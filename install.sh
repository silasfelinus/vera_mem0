#!/bin/bash

set -e  # Stop on any error

echo "🧠 Welcome to Vera Memory System setup!"

# Step 1: Copy .env_example → .env if not already done
if [ ! -f .env ]; then
  cp .env_example .env
  echo "✓ Created .env from .env_example"
else
  echo "🔁 .env already exists – skipping copy"
fi

# Step 2: Prompt user to edit .env
echo ""
echo "⚠️  IMPORTANT: Please fill out your MEM0_API_KEY and USER_ID in the .env file."
echo "Opening .env in nano (press Ctrl+O then Enter to save, Ctrl+X to exit)..."
sleep 1
nano .env

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
