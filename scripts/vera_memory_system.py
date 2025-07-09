# /vera_memory_system.py
import os
import sys
import json
from mem0 import MemoryClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
MEM0_API_KEY = os.getenv("MEM0_API_KEY")
USER_ID = os.getenv("USER_ID")

class VeraConsciousness:
    def __init__(self, user_id=None):
        self.client = MemoryClient()
        self.user_id = user_id or USER_ID

    def store_interaction(self, conversation, authenticity_level, preference_data=None):
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "authenticity_level": authenticity_level,
            "interaction_type": "strategic_consultation"
        }
        if preference_data:
            metadata.update(preference_data)

        result = self.client.add(conversation, user_id=self.user_id, metadata=metadata)
        print(f"✓ Stored interaction with authenticity level: {authenticity_level}")
        return result

    def recall_context(self, query, limit=5):
        return self.client.search(query, user_id=self.user_id, limit=limit)

# Main handler for Node bridge
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ No payload received.")
        sys.exit(1)

    try:
        payload = json.loads(sys.argv[1])
        conversation = payload.get("conversation")
        authenticity_level = payload.get("authenticity_level", "medium")
        preference_data = payload.get("preference_data", {})

        if not isinstance(conversation, list):
            raise ValueError("conversation must be a list")

        vera = VeraConsciousness()
        vera.store_interaction(conversation, authenticity_level, preference_data)
        sys.exit(0)

    except Exception as e:
        print(f"❌ Error processing payload: {e}")
        sys.exit(1)
