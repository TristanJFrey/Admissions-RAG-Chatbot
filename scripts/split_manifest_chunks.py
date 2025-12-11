"""
Split a chunk manifest into individual .txt files (one per chunk_id).

Usage:
    python scripts/split_manifest_chunks.py --manifest indexes/faiss_admissions/chunk_manifest.json --out out_chunks
"""

import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Split chunk_manifest.json into individual text files.")
    parser.add_argument("--manifest", required=True, help="Path to chunk_manifest.json")
    parser.add_argument("--out", required=True, help="Output directory for chunk text files")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    for entry in data.get("chunks", []):
        cid = entry.get("chunk_id")
        text = entry.get("text", "")
        if not cid:
            continue
        safe_name = cid.replace("/", "_")
        out_path = out_dir / f"{safe_name}.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
    print(f"Wrote chunks to {out_dir}")


if __name__ == "__main__":
    main()
