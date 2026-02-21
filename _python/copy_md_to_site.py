import os
import shutil
from pathlib import Path

# Source directories to scan for .md files
dirs = ["_posts", "_pages"]
site_dir = Path("_site")

for src_dir in dirs:
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".md"):
                src_path = Path(root) / file
                # Build the slug (Jekyll's default: :title)
                # Remove date prefix if present (e.g. 2024-12-29-title.md)
                name = file
                if src_dir == "_posts" and "-" in file:
                    name = "-".join(file.split("-")[3:]) or file
                # Remove .md extension
                slug = name[:-3]
                # Output path
                dest_path = site_dir / f"{slug}.md"
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dest_path)
                print(f"Copied {src_path} -> {dest_path}")
