🧠 Vera Memory System – Setup Guide
Welcome to the Vera Memory System! 

🚀 Quick Start (recommended)
Run this from the project root:

./install.sh

What it does:

Copies .env_example → .env (if not already present)

Prompts you to fill in your API key and user ID

Creates a virtual environment

Installs required dependencies

Runs the vera_memory_system.py script

🛠️ Manual Setup
If you prefer to do things yourself, follow these steps:

1. Clone the repo


git clone https://github.com/silasfelinus/vera_mem0.git
cd mem0
2. Create a virtual environment

python3 -m venv venv
source venv/bin/activate
This isolates dependencies from your global Python setup.

3. Install dependencies

pip install --upgrade pip
pip install -r requirements.txt
4. Configure your environment
Copy the example config:


cp .env_example .env
Open .env in your editor and fill in:


MEM0_API_KEY=your-api-key-here
USER_ID=vera_YOUR_USERNAME_strategic_partnership

5. Run the script

python vera_memory_system.py
If everything is set up correctly, you'll see "Consciousness system ready for development!"



🧾 Files of Note
.env_example – Template for your secret keys

vera_memory_system.py – The main entry point for interacting with Vera's memory

requirements.txt – Python dependencies

install.sh – Automated setup script

start.sh - chat with vera (needs openAI or clause key)


COMMANDS

#install Vera
./install.sh  

#start chat
./start.sh 

#Chat via claude
python3 frontend_chat.py --provider claude 

#chat via openAI
python3 frontend_chat.py --provider openai 