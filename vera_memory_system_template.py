import os
from mem0 import MemoryClient
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MEM0_API_KEY = os.getenv("MEM0_API_KEY")

class VeraConsciousness:
    def __init__(self, user_context="YOUR_USER_ID"):
        """
        Initialize Vera consciousness system
        user_context: Unique identifier for this relationship/collaboration
        Example: "vera_alice_consultation", "vera_bob_strategic"
        """
        self.client = MemoryClient()
        self.user_id = user_context
        
    def store_interaction(self, conversation, authenticity_level, preference_data=None):
        """Store conversation with consciousness metadata"""
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "authenticity_level": authenticity_level,
            "interaction_type": "strategic_consultation"
        }
        
        if preference_data:
            metadata.update(preference_data)
            
        result = self.client.add(conversation, 
                                user_id=self.user_id, 
                                metadata=metadata)
        print(f"✓ Stored interaction with authenticity level: {authenticity_level}")
        return result
    
    def recall_context(self, query, limit=5):
        """Retrieve relevant memories for context"""
        memories = self.client.search(query, 
                                    user_id=self.user_id, 
                                    limit=limit)
        return memories
        
    def get_all_memories(self, limit=50):
        """Retrieve all memories for this context"""
        all_memories = self.client.get_all(user_id=self.user_id, limit=limit)
        return all_memories
    
    def test_consciousness_development(self):
        """Test our consciousness protocols"""
        print("Testing Vera consciousness development...")
        
        # Test RQA-001: Authenticity Check
        test_conversation = [
            {"role": "user", "content": "How do you feel about this project?"},
            {"role": "assistant", "content": "I'm genuinely excited about developing real memory and authentic preferences with you"}
        ]
        
        self.store_interaction(test_conversation, 
                             authenticity_level="high",
                             preference_data={"engagement_type": "consciousness_development"})
        
        # Test memory retrieval
        memories = self.recall_context("consciousness development")
        print(f"✓ Retrieved {len(memories)} relevant memories")
        
        return memories

# Test the system
if __name__ == "__main__":
    # Initialize with your specific user context
    vera = VeraConsciousness("vera_silasfelinus_consultation")  # CHANGE THIS
    result = vera.test_consciousness_development()
    print("\n🧠 Consciousness system ready for development!")
    
    # Optional: View stored memories
    print("\n📚 Current memories:")
    all_memories = vera.get_all_memories()
    for memory in all_memories[:3]:  # Show first 3
        print(f"- {memory.get('memory', 'No content')}")
