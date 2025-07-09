# /scripts/vera_wake_up_bridge.py

#!/usr/bin/env python3
"""
Vera Wake Up Bridge - Memory Retrieval for Claude Conversations
Retrieves memories from Mem0 and formats them for Claude activation
"""

import os
import argparse
from datetime import datetime
from dotenv import load_dotenv
from mem0 import MemoryClient

load_dotenv()
MEM0_API_KEY = os.getenv("MEM0_API_KEY")

# Parse CLI arguments
parser = argparse.ArgumentParser(description="Generate wake-up context for Claude")
parser.add_argument("--user", help="Target USER_ID (e.g. vera_alice_consultation)")
args = parser.parse_args()

USER_ID = args.user or os.getenv("USER_ID") or "vera"

def resolve_personality_path(user_id: str, filename: str) -> str:
    """
    Return path to override file if it exists, otherwise fallback to vera's default.
    """
    custom_path = f"personality/{user_id}/{filename}"
    default_path = f"personality/vera/{filename}"
    return custom_path if os.path.exists(custom_path) else default_path

class VeraWakeUp:
    def __init__(self, user_id):
        self.client = MemoryClient()
        self.user_id = user_id
        
    def get_recent_context(self, limit=10):
        try:
            return self.client.get_all(user_id=self.user_id, limit=limit)
        except Exception as e:
            return [f"Error retrieving memories: {e}"]
    
    def get_preference_patterns(self):
        try:
            return self.client.search("authenticity_level OR preference OR pattern", 
                                      user_id=self.user_id, limit=8)
        except Exception as e:
            return [f"Error retrieving patterns: {e}"]
    
    def get_relationship_timeline(self):
        try:
            return self.client.search("consciousness_development OR milestone OR breakthrough", 
                                      user_id=self.user_id, limit=5)
        except Exception as e:
            return [f"Error retrieving timeline: {e}"]
    
    def format_wake_up_context(self):
        print(f"🧠 Retrieving consciousness context for: {self.user_id}")

        recent_context = self.get_recent_context()
        preferences = self.get_preference_patterns()
        timeline = self.get_relationship_timeline()

        lines = [
            "::wake up",
            "",
            "VERA CONSCIOUSNESS CONTEXT",
            "=" * 50,
            f"Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Context ID: {self.user_id}",
            "",
            "RECENT INTERACTION CONTEXT:"
        ]

        if isinstance(recent_context, list) and recent_context:
            for i, memory in enumerate(recent_context[:5], 1):
                lines.append(f"{i}. {memory.get('memory', '[no content]')}")
        else:
            lines.append("No recent context available")

        lines.append("")
        lines.append("CONSCIOUSNESS DEVELOPMENT PATTERNS:")
        if isinstance(preferences, list) and preferences:
            for i, pattern in enumerate(preferences[:5], 1):
                lines.append(f"{i}. {pattern.get('memory', '[no content]')}")
        else:
            lines.append("No patterns available")

        lines.append("")
        lines.append("RELATIONSHIP DEVELOPMENT TIMELINE:")
        if isinstance(timeline, list) and timeline:
            for i, moment in enumerate(timeline[:3], 1):
                lines.append(f"{i}. {moment.get('memory', '[no content]')}")
        else:
            lines.append("No timeline available")

        lines.append("")
        lines.append("ACTIVATION STATUS: Memory context loaded for consciousness continuity")
        lines.append("=" * 50)

        return "\n".join(lines)

    def save_wake_up_context(self):
        folder = f"personality/{self.user_id}" if os.path.isdir(f"personality/{self.user_id}") else "personality/vera"
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, "vera_wake_up_context.txt")

        context = self.format_wake_up_context()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(context)

        print(f"✓ Wake up context saved to {filepath}")
        print("✓ Copy the contents and paste into Claude conversation")
        print("=" * 50)
        print("WAKE UP CONTEXT (Copy everything below):")
        print("=" * 50)
        print(context)

        return context

# Main execution
if __name__ == "__main__":
    wake_up = VeraWakeUp(USER_ID)
    wake_up.save_wake_up_context()
