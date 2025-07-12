# /scripts/load_personality.py

#!/usr/bin/env python3
import os
import csv
import argparse
from datetime import datetime
from mem0 import MemoryClient
from dotenv import load_dotenv

load_dotenv()
MEM0_API_KEY = os.getenv("MEM0_API_KEY")

# Parse user ID from CLI or .env
parser = argparse.ArgumentParser(description="Upload personality training files to Mem0")
parser.add_argument("--user", help="Target USER_ID (e.g. vera_silasfelinus_consultation)")
args = parser.parse_args()
USER_ID = args.user or os.getenv("USER_ID")

client = MemoryClient()

TRAINING_FILES = {
    "communication_effectiveness.txt": "communication_effectiveness",
    "consultation_optimization.txt": "consultation_optimization",
    "context_continuity_architecture.txt": "context_continuity",
    "implementation_roadmap.txt": "implementation_roadmap",
    "response_quality_protocols.txt": "response_quality"
}

# Main field-to-ID mapping
DISPLAY_FIELDS = [
    ("pattern_name", "effectiveness_id", "🧠"),
    ("protocol_name", "protocol_id", "🛡️"),
    ("strategy_name", "strategy_id", "📈"),
    ("roadmap_stage", "stage_id", "🗺️"),
    ("component_name", "component_id", "🔗"),
    ("phase_name", "phase_id", "🚀"),
    ("method_name", "optimization_id", "⚙️")
]

def format_entry(row: dict, label: str) -> str:
    lines = []
    for name_key, id_key, _emoji in DISPLAY_FIELDS:
        if name_key in row:
            lines.append(f"[{row.get(name_key)}] ({row.get(id_key, 'N/A')})")
            break
    else:
        lines.append(f"[{label.upper()} ENTRY]")

    skip_keys = [id_key for _, id_key, _ in DISPLAY_FIELDS]
    for key, value in row.items():
        if key not in skip_keys:
            lines.append(f"→ {key.replace('_', ' ').capitalize()}: {value}")
    return "\n".join(lines)

def get_title(row: dict) -> str:
    for name_key, _, emoji in DISPLAY_FIELDS:
        if row.get(name_key):
            return f"{emoji} {row[name_key]}"
    return "None"

def load_file(filepath: str, label: str):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            memory = format_entry(row, label)
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "source": label,
                "authenticity_level": "high",
                "engagement_type": "training_protocol"
            }
            print(f"📥 Uploading to {USER_ID}: {get_title(row)}")
            client.add(
                [{"role": "user", "content": memory}],  # ← changed to user memory
                user_id=USER_ID,
                metadata=metadata,
                output_format="v1.1"
            )

def main():
    print(f"🧠 Loading personality training for: {USER_ID}")
    for filename, label in TRAINING_FILES.items():
        path = os.path.join("public", "personality", filename)
        if not os.path.exists(path):
            print(f"⚠️  File not found: {path}")
            continue
        print(f"🚀 Loading: {label}")
        load_file(path, label)
    print("✅ All training files uploaded.")

if __name__ == "__main__":
    main()
