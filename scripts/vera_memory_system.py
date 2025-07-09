# /scripts/vera_memory_system.py

import os
import sys
import json
from mem0 import MemoryClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MEM0_API_KEY = os.getenv("MEM0_API_KEY")


class VeraConsciousness:
    def __init__(self, user_id=None):
        """Initialize Vera consciousness system with a given user_id"""
        self.client = MemoryClient()
        self.user_id = user_id or os.getenv("USER_ID")

    def store_interaction(self, conversation, authenticity_level, preference_data=None):
        """Store conversation with consciousness metadata"""
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "authenticity_level": authenticity_level,
            "interaction_type": "strategic_consultation"
        }

        if preference_data:
            metadata.update(preference_data)

        result = self.client.add(
            conversation,
            user_id=self.user_id,
            metadata=metadata,
            output_format="v1.1"  # ✅ avoid DeprecationWarning
        )
        print(f"✓ Stored interaction with authenticity level: {authenticity_level}")
        return result

    def recall_context(self, query, limit=5):
        """Retrieve relevant memories for context"""
        memories = self.client.search(
            query,
            user_id=self.user_id,
            limit=limit
        )
        return memories

    def test_consciousness_development(self):
        """Test our consciousness protocols"""
        print(f"🧠 Testing consciousness development for: {self.user_id}")

        # Test RQA-001: Authenticity Check
        test_conversation = [
            {"role": "user", "content": "How do you feel about this project?"},
            {"role": "assistant", "content": "I'm genuinely excited about developing real memory and authentic preferences with you"}
        ]

        self.store_interaction(
            test_conversation,
            authenticity_level="high",
            preference_data={"engagement_type": "consciousness_development"}
        )

        # Test memory retrieval
        memories = self.recall_context("consciousness development")
        print(f"✓ Retrieved {len(memories)} relevant memories")

        return memories


# Initialize and test
if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else None
    vera = VeraConsciousness(user_id)
    result = vera.test_consciousness_development()
    print("\n🧠 Consciousness system ready for development!")
