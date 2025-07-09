# /scripts/load_personality.py

#!/usr/bin/env python3
import os
import csv
from datetime import datetime
from mem0 import MemoryClient
from dotenv import load_dotenv

load_dotenv()

MEM0_API_KEY = os.getenv("MEM0_API_KEY")
USER_ID = os.getenv("USER_ID")

client = MemoryClient()

# Files to load and their tag labels
TRAINING_FILES = {
    "communication_effectiveness.txt": "communication_effectiveness",
    "consultation_optimization.txt": "consultation_optimization",
    "context_continuity_architecture.txt": "context_continuity",
    "implementation_roadmap.txt": "implementation_roadmap",
    "response_quality_protocols.txt": "response_quality"
}

def format_entry(row: dict, label: str) -> str:
    # Use keys dynamically in case structure varies slightly between files
    lines = []
    if "pattern_name" in row:
        lines.append(f"[{row.get('pattern_name')}] ({row.get('effectiveness_id', 'N/A')})")
    elif "protocol_name" in row:
        lines.append(f"[{row.get('protocol_name')}] ({row.get('protocol_id', 'N/A')})")
    elif "strategy_name" in row:
        lines.append(f"[{row.get('strategy_name')}] ({row.get('strategy_id', 'N/A')})")
    elif "roadmap_stage" in row:
        lines.append(f"[{row.get('roadmap_stage')}] ({row.get('stage_id', 'N/A')})")
    elif "continuity_type" in row:
        lines.append(f"[{row.get('continuity_type')}] ({row.get('architecture_id', 'N/A')})")
    else:
        lines.append(f"[{label.upper()} ENTRY]")

    for key, value in row.items():
        if key not in ["effectiveness_id", "protocol_id", "strategy_id", "stage_id", "architecture_id"]:
            lines.append(f"→ {key.replace('_', ' ').capitalize()}: {value}")
    return "\n".join(lines)

def load_file(filepath: str, label: str):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            memory = format_entry(row, label)
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "source": label,
                "authenticity_level": "system",
                "engagement_type": "training_protocol"
            }
            print(f"📥 Uploading: {row.get('pattern_name') or row.get('protocol_name') or row.get('strategy_name') or row.get('roadmap_stage') or row.get('continuity_type')}")
            client.add([{"role": "system", "content": memory}], user_id=USER_ID, metadata=metadata)

def main():
    print("🧠 Loading Vera personality training files...")
    for filename, label in TRAINING_FILES.items():
        path = os.path.join("personality", filename)
        if not os.path.exists(path):
            print(f"⚠️  File not found: {path}")
            continue
        print(f"🚀 Loading: {label}")
        load_file(path, label)
    print("✅ All training files uploaded.")

if __name__ == "__main__":
    main()
