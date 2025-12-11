import argparse
import json
import os
import re
import sys
from typing import Dict, List, Tuple, Optional

from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document

RetrieverHit = Tuple[object, float]  # (Document, raw_score)


def tokenize(text: str) -> List[str]:
    return re.findall(r"\b\w+\b", text.lower())


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hybrid FAISS + BM25 search with Reciprocal Rank Fusion.")
    parser.add_argument("--index", required=True, help="Path to FAISS index directory")
    parser.add_argument("--doc", required=True, help="Path to DOCX source used for BM25 retrieval")
    parser.add_argument("--q", required=True, help="Query text")
    parser.add_argument("--k", type=int, default=5, help="Number of final hybrid results to display")
    parser.add_argument("--faiss_k", type=int, default=10, help="How many FAISS hits to pull before fusion")
    parser.add_argument("--bm25_k", type=int, default=10, help="How many BM25 hits to pull before fusion")
    parser.add_argument("--rrf_k", type=int, default=60, help="k constant for Reciprocal Rank Fusion")
    parser.add_argument("--chunk_size", type=int, default=1200, help="Chunk size for BM25 splitter (match ingestion)")
    parser.add_argument("--chunk_overlap", type=int, default=200, help="Chunk overlap for BM25 splitter (match ingestion)")
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2", help="Embedding model for FAISS")
    parser.add_argument("--manifest", help="Optional chunk manifest JSON from ingestion (avoids re-splitting)")
    return parser


def load_faiss_hits(index_dir: str, query: str, model_name: str, top_k: int) -> List[RetrieverHit]:
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vs = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
    return vs.similarity_search_with_score(query, k=top_k)


def load_bm25_hits(
    doc_path: str,
    query: str,
    top_k: int,
    chunk_size: int,
    chunk_overlap: int,
    manifest_path: Optional[str] = None,
) -> List[RetrieverHit]:
    chunks: List[Tuple[object, str]] = []
    tokenized_corpus: List[List[str]] = []

    manifest_chunks = _load_chunks_from_manifest(manifest_path) if manifest_path else None
    if manifest_chunks:
        for entry in manifest_chunks:
            text = entry.page_content.strip()
            if not text:
                continue
            chunks.append((entry, text))
            tokenized_corpus.append(tokenize(text))
    else:
        if not os.path.exists(doc_path):
            raise FileNotFoundError(f"Document not found: {doc_path}")

        docs = Docx2txtLoader(doc_path).load()
        for i, d in enumerate(docs):
            d.metadata.update({"source": os.path.basename(doc_path), "doc_id": f"{os.path.basename(doc_path)}-{i}"})

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )
        split_chunks = splitter.split_documents(docs)

        for idx, chunk in enumerate(split_chunks):
            chunk.metadata["chunk_id"] = f"{chunk.metadata['doc_id']}-chunk-{idx:05d}"
            text = chunk.page_content.strip()
            if not text:
                continue
            chunks.append((chunk, text))
            tokenized_corpus.append(tokenize(text))

    if not chunks:
        return []

    bm25 = BM25Okapi(tokenized_corpus)
    query_tokens = tokenize(query)
    scores = bm25.get_scores(query_tokens)

    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    hits: List[RetrieverHit] = []
    for rank, idx in enumerate(ranked_indices, start=1):
        chunk, _ = chunks[idx]
        hits.append((chunk, scores[idx]))
    return hits


def _load_chunks_from_manifest(manifest_path: str) -> Optional[List[Document]]:
    if not manifest_path or not os.path.exists(manifest_path):
        return None
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        items = []
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
            items.append(Document(page_content=text, metadata=meta))
        return items
    except Exception:
        return None


def reciprocal_rank_fusion(
    faiss_hits: List[RetrieverHit],
    bm25_hits: List[RetrieverHit],
    rrf_k: int,
    final_k: int,
):
    accumulator: Dict[str, Dict] = {}

    def register(hit_doc, raw_score, retriever_name: str, rank: int):
        chunk_id = hit_doc.metadata.get("chunk_id") or f"{retriever_name}-{rank}"
        entry = accumulator.setdefault(
            chunk_id,
            {
                "doc": hit_doc,
                "retrievals": {},
                "rrf_score": 0.0,
            },
        )
        entry["retrievals"][retriever_name] = {"rank": rank, "score": raw_score}
        entry["rrf_score"] += 1.0 / (rrf_k + rank)

    for rank, (doc, raw_score) in enumerate(faiss_hits, start=1):
        register(doc, raw_score, "faiss", rank)
    for rank, (doc, raw_score) in enumerate(bm25_hits, start=1):
        register(doc, raw_score, "bm25", rank)

    ordered = sorted(accumulator.values(), key=lambda x: x["rrf_score"], reverse=True)
    return ordered[:final_k]


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    manifest_path = args.manifest
    if not manifest_path:
        candidate = os.path.join(args.index, "chunk_manifest.json")
        manifest_path = candidate if os.path.exists(candidate) else None

    faiss_hits = load_faiss_hits(args.index, args.q, args.model, args.faiss_k)
    bm25_hits = load_bm25_hits(args.doc, args.q, args.bm25_k, args.chunk_size, args.chunk_overlap, manifest_path=manifest_path)
    fused = reciprocal_rank_fusion(faiss_hits, bm25_hits, args.rrf_k, args.k)

    print(f"\n=== Hybrid RRF Results (top {len(fused)}) for: '{args.q}' ===")
    for rank, entry in enumerate(fused, start=1):
        doc = entry["doc"]
        meta = doc.metadata
        retrievals = entry["retrievals"]
        print(f"\n--- Result #{rank} ---")
        print(f"chunk_id : {meta.get('chunk_id')}")
        print(f"source   : {meta.get('source')}")
        print(f"RRF score: {entry['rrf_score']:.4f}")

        faiss_info = retrievals.get("faiss")
        bm25_info = retrievals.get("bm25")
        print(f"FAISS    : {_format_retrieval_info(faiss_info)}")
        print(f"BM25     : {_format_retrieval_info(bm25_info)}")
        print(f"text     : {_preview_text(doc.page_content.strip())}")


def _format_retrieval_info(info: Dict) -> str:
    if not info:
        return "n/a"
    return f"rank {info['rank']} (score {info['score']:.4f})"


def _preview_text(text: str) -> str:
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    return text.encode(encoding, errors="replace").decode(encoding, errors="replace")


if __name__ == "__main__":
    main()
