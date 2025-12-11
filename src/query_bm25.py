"""
query_bm25.py

Lexical (keyword-based) search over a DOCX or JSON document using BM25.

Usage:
    python src/query_bm25.py --doc data/admissions.docx --q "when is the undergrad admissions deadline?" --k 5
"""

import argparse
import json
import os
import re
import sys
from typing import Optional, List, Tuple
from rank_bm25 import BM25Okapi
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def tokenize(text: str):
    """Simple whitespace + punctuation tokenizer."""
    return re.findall(r"\b\w+\b", text.lower())

def main():
    parser = argparse.ArgumentParser(description="Query DOCX using BM25 keyword matching.")
    parser.add_argument("--doc", required=True, help="Path to DOCX or JSON file")
    parser.add_argument("--q", required=True, help="Query text")
    parser.add_argument("--k", type=int, default=5, help="Number of top results")
    parser.add_argument("--chunk_size", type=int, default=1200, help="Chunk size for splitting")
    parser.add_argument("--chunk_overlap", type=int, default=200, help="Overlap between chunks")
    parser.add_argument("--manifest", help="Optional chunk manifest JSON from ingestion to avoid re-splitting")
    args = parser.parse_args()

    manifest = args.manifest
    if not manifest:
        candidate = os.path.join(os.path.dirname(os.path.abspath(args.doc)), "chunk_manifest.json")
        manifest = candidate if os.path.exists(candidate) else None

    chunks = _load_chunks_from_manifest(manifest)
    if not chunks:
        if not os.path.exists(args.doc):
            sys.exit(f"File not found: {args.doc}")

        docs = Docx2txtLoader(args.doc).load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )
        docs = splitter.split_documents(docs)
        for idx, c in enumerate(docs):
            c.metadata.setdefault("doc_id", f"{os.path.basename(args.doc)}-0")
            c.metadata["chunk_id"] = f"{c.metadata['doc_id']}-chunk-{idx:05d}"
        chunks = docs

    texts = [c.page_content.strip() for c in chunks if c.page_content.strip()]
    tokenized_corpus = [tokenize(t) for t in texts]
    bm25 = BM25Okapi(tokenized_corpus)

    query_tokens = tokenize(args.q)
    scores = bm25.get_scores(query_tokens)

    # Rank top-k matches
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:args.k]

    print(f"\n=== Top {args.k} BM25 Results for: '{args.q}' ===")
    for rank, idx in enumerate(ranked_indices, start=1):
        chunk = chunks[idx]
        text = texts[idx]
        meta = getattr(chunk, "metadata", {}) or {}
        print(f"\n--- Result #{rank} ---")
        print(f"Score : {scores[idx]:.4f}")
        print(f"Chunk : {meta.get('chunk_id', 'n/a')}")
        print(f"Text  : {_preview_text(text)}")

def _preview_text(text: str) -> str:
    """Clamp encoding to avoid Windows cp1252 issues."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    safe = text.encode(encoding, errors="replace").decode(encoding, errors="replace")
    # Shorten text preview
    # if len(safe) > 400:
    #     safe = safe[:400] + "..."
    return safe


def _load_chunks_from_manifest(manifest_path: Optional[str]) -> List[Document]:
    if not manifest_path or not os.path.exists(manifest_path):
        return []
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        chunks = []
        for entry in payload.get("chunks", []):
            text = entry.get("text", "")
            chunk_id = entry.get("chunk_id")
            if not text or not chunk_id:
                continue
            meta = {
                "chunk_id": chunk_id,
                "doc_id": entry.get("doc_id"),
                "source": entry.get("source"),
            }
            chunks.append(Document(page_content=text, metadata=meta))
        return chunks
    except Exception:
        return []

if __name__ == "__main__":
    main()
