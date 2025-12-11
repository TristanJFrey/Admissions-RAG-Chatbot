"""
answer_hybrid_rag.py

Run hybrid retrieval (FAISS + BM25 + RRF), then generate an answer with citations
using a Hugging Face text2text model (default: google/flan-t5-base).

Example:
    python src/answer_hybrid_rag.py --index indexes/faiss_admissions --doc data/admissions.md --manifest indexes/faiss_admissions/chunk_manifest.json --q "When is the undergrad application deadline?" --k 4 --faiss_k 10 --bm25_k 10 --max_new_tokens 200
"""

import argparse
import os
from typing import List

from transformers import pipeline

from query_hybrid_rrf import (
    load_faiss_hits,
    load_bm25_hits,
    reciprocal_rank_fusion,
)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hybrid RAG answer generator with citations.")
    parser.add_argument("--index", required=True, help="Path to FAISS index directory")
    parser.add_argument("--doc", required=True, help="Path to DOCX source used for BM25 retrieval")
    parser.add_argument("--q", required=True, help="User question")
    parser.add_argument("--k", type=int, default=4, help="Number of fused chunks to pass to the generator")
    parser.add_argument("--faiss_k", type=int, default=10, help="FAISS hits to fetch before fusion")
    parser.add_argument("--bm25_k", type=int, default=10, help="BM25 hits to fetch before fusion")
    parser.add_argument("--rrf_k", type=int, default=60, help="RRF k constant")
    parser.add_argument("--chunk_size", type=int, default=1200, help="Chunk size for BM25 splitter (match ingest)")
    parser.add_argument("--chunk_overlap", type=int, default=200, help="Chunk overlap for BM25 splitter (match ingest)")
    parser.add_argument("--embedding_model", default="sentence-transformers/all-MiniLM-L6-v2", help="Embedding model used for FAISS queries")
    parser.add_argument("--manifest", help="Optional chunk manifest JSON from ingestion (avoids re-splitting)")
    parser.add_argument("--gen_model", default="google/flan-t5-base", help="HF text2text model id")
    parser.add_argument("--max_new_tokens", type=int, default=200, help="Max tokens to generate")
    parser.add_argument("--num_beams", type=int, default=4, help="Beam search width to reduce repetition")
    return parser


def load_generator(model_id: str, num_beams: int, max_new_tokens: int):
    """Create a lightweight text2text pipeline. Defaults to CPU unless GPU is available."""
    generator = pipeline(
        "text2text-generation",
        model=model_id,
        truncation=True,
    )
    # wrap to inject params each call
    def run(prompt: str):
        return generator(
            prompt,
            max_new_tokens=max_new_tokens,
            num_beams=num_beams,
            no_repeat_ngram_size=4,
            repetition_penalty=1.2,
        )[0]["generated_text"]
    return run


def build_prompt(question: str, contexts: List[str], chunk_ids: List[str]) -> str:
    context_block = "\n\n".join([f"[{cid}] {text}" for cid, text in zip(chunk_ids, contexts)])
    return (
        "You are an admissions assistant. Answer in one short, direct sentence using ONLY the provided context. "
        "Cite chunk ids inline in brackets (e.g., [admissions.md-0-chunk-00002]). "
        "Do not list tables verbatim. If the answer is not in the context, say you do not have that information.\n\n"
        f"Question: {question}\n\n"
        f"Context:\n{context_block}\n\n"
        "Answer:"
    )


def _ensure_citation(answer: str, chunk_ids: List[str]) -> str:
    """If the model forgot to cite, append the top chunk id as a minimal citation."""
    for cid in chunk_ids:
        if cid and cid in answer:
            return answer
    if not chunk_ids:
        return answer
    suffix = f" [{chunk_ids[0]}]"
    if answer.endswith((".", "!", "?")):
        return answer + suffix
    return answer + suffix


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    manifest_path = args.manifest
    if not manifest_path:
        candidate = os.path.join(args.index, "chunk_manifest.json")
        manifest_path = candidate if os.path.exists(candidate) else None

    faiss_hits = load_faiss_hits(args.index, args.q, args.embedding_model, args.faiss_k)
    bm25_hits = load_bm25_hits(args.doc, args.q, args.bm25_k, args.chunk_size, args.chunk_overlap, manifest_path=manifest_path)
    fused = reciprocal_rank_fusion(faiss_hits, bm25_hits, args.rrf_k, args.k)

    if not fused:
        print("No retrieved context; cannot generate an answer.")
        return

    top_docs = fused[: args.k]
    contexts = [entry["doc"].page_content.strip() for entry in top_docs]
    chunk_ids = [entry["doc"].metadata.get("chunk_id", f"chunk-{i}") for i, entry in enumerate(top_docs)]

    prompt = build_prompt(args.q, contexts, chunk_ids)
    generate = load_generator(args.gen_model, args.num_beams, args.max_new_tokens)
    raw_answer = generate(prompt)
    # Strip any accidental "Sources" echoes from the model output.
    answer = raw_answer.split("Sources:")[0].strip()

    answer = _ensure_citation(answer, chunk_ids)

    print("\n=== Hybrid RAG Answer ===")
    print(answer.strip())
    print("\nSources:")
    for cid, text in zip(chunk_ids, contexts):
        preview = text.replace("\n", " ")
        if len(preview) > 220:
            preview = preview[:220] + "..."
        print(f"- {cid}: {preview}")


if __name__ == "__main__":
    main()
