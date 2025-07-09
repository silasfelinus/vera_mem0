# /scripts/tag_file_paths.py

#!/usr/bin/env python3

import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TARGET_EXTENSIONS = {'.py', '.txt', '.csv'}

IGNORE_PATTERNS = [
    "node_modules", ".nuxt", "nuxt", ".nitro", ".cache", ".output", "dist",
    "venv", ".venv", ".DS_Store", ".env", "backup.json", "_nuxt",
    ".yarn", "yarn", ".users.http", "*.log", "*.pem", "*.http", "*.env",
    "mnt/appdata", "portfolio/.yarn", "portfolio/yarn", "cypress.env.json",
    "cypress/screenshots", "http-client.env.json", "utils/.users.http"
]

def is_ignored(path: Path) -> bool:
    path_str = str(path.relative_to(ROOT_DIR)).replace("\\", "/")

    for pattern in IGNORE_PATTERNS:
        if pattern.endswith("/*") and pattern[:-2] in path_str:
            return True
        if pattern.startswith("*") and path_str.endswith(pattern[1:]):
            return True
        if path_str.startswith(pattern) or f"/{pattern}/" in path_str:
            return True
        if Path(path_str).match(pattern):
            return True
    return False

def get_path_comment(filepath: Path) -> str:
    return f"# /{filepath.relative_to(ROOT_DIR).as_posix()}"

def process_file(filepath: Path):
    if is_ignored(filepath):
        return

    if filepath.suffix not in TARGET_EXTENSIONS:
        return

    try:
        lines = filepath.read_text(encoding='utf-8').splitlines()
    except Exception as e:
        print(f"⚠️ Could not read {filepath}: {e}")
        return

    comment = get_path_comment(filepath)
    existing_comment = lines[0] if lines else ""

    if existing_comment.strip() == comment:
        # Ensure second line is blank
        if len(lines) > 1 and lines[1].strip() != "":
            lines.insert(1, "")
        elif len(lines) == 1:
            lines.append("")
    else:
        if existing_comment.startswith("# /"):
            lines[0] = comment
        else:
            lines.insert(0, comment)
        lines.insert(1, "")  # ensure blank line after comment

    try:
        filepath.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        print(f"✓ Updated: {filepath.relative_to(ROOT_DIR)}")
    except Exception as e:
        print(f"❌ Failed to write {filepath}: {e}")

def main():
    print("🔍 Scanning for source files...")
    for root, _, filenames in os.walk(ROOT_DIR):
        for name in filenames:
            path = Path(root) / name
            process_file(path)
    print("✅ All eligible files updated.")

if __name__ == "__main__":
    main()
