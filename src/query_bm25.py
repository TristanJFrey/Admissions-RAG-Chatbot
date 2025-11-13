"""
query_bm25.py

Lexical (keyword-based) search over a DOCX or JSON document using BM25.

Usage:
    python src/query_bm25.py --doc data/admissions.docx --q "when is the undergrad admissions deadline?" --k 5
"""

import os
import re
import sys
import argparse
from rank_bm25 import BM25Okapi
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
    args = parser.parse_args()

    if not os.path.exists(args.doc):
        sys.exit(f"File not found: {args.doc}")

    # Load DOCX as LangChain Documents
    docs = Docx2txtLoader(args.doc).load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    texts = [c.page_content.strip() for c in chunks if c.page_content.strip()]

    # Tokenize corpus and query
    tokenized_corpus = [tokenize(t) for t in texts]
    bm25 = BM25Okapi(tokenized_corpus)

    query_tokens = tokenize(args.q)
    scores = bm25.get_scores(query_tokens)

    # Rank top-k matches
    ranked = sorted(zip(texts, scores), key=lambda x: x[1], reverse=True)[:args.k]

    print(f"\n=== Top {args.k} BM25 Results for: '{args.q}' ===")
    for rank, (text, score) in enumerate(ranked, start=1):
        print(f"\n--- Result #{rank} ---")
        print(f"Score : {score:.4f}")
        print(f"Text  : {_preview_text(text)}")

def _preview_text(text: str) -> str:
    """Clamp encoding to avoid Windows cp1252 issues."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    safe = text.encode(encoding, errors="replace").decode(encoding, errors="replace")
    # Shorten text preview
    # if len(safe) > 400:
    #     safe = safe[:400] + "..."
    return safe

if __name__ == "__main__":
    main()
