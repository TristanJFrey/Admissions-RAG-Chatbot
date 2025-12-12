"""
answer_hybrid_rag.py

Run hybrid retrieval (FAISS + BM25 + RRF), then generate an answer with citations
using a generator model (default: Google Gemini, e.g., gemini-2.5-flash-lite; requires GOOGLE_API_KEY).

Example:
    python src/answer_hybrid_rag.py --index indexes/faiss_admissions --doc data/admissions.md --manifest indexes/faiss_admissions/chunk_manifest.json --q "When is the undergrad application deadline?" --k 4 --faiss_k 10 --bm25_k 10 --max_new_tokens 200
"""

import argparse
import os
import re
from typing import List

from dotenv import load_dotenv
from transformers import pipeline, AutoConfig, AutoTokenizer

from query_hybrid_rrf import (
    load_faiss_hits,
    load_bm25_hits,
    reciprocal_rank_fusion,
)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hybrid RAG answer generator with citations.")
    parser.add_argument("--index", required=True, help="Path to FAISS index directory")
    parser.add_argument("--doc", required=True, help="Path to source file used for BM25 retrieval (md/docx)")
    parser.add_argument("--q", required=True, help="User question")
    parser.add_argument("--k", type=int, default=4, help="Number of fused chunks to pass to the generator")
    parser.add_argument("--faiss_k", type=int, default=10, help="FAISS hits to fetch before fusion")
    parser.add_argument("--bm25_k", type=int, default=10, help="BM25 hits to fetch before fusion")
    parser.add_argument("--rrf_k", type=int, default=60, help="RRF k constant")
    parser.add_argument("--chunk_size", type=int, default=1200, help="Chunk size for BM25 splitter (match ingest)")
    parser.add_argument("--chunk_overlap", type=int, default=200, help="Chunk overlap for BM25 splitter (match ingest)")
    parser.add_argument("--embedding_model", default="sentence-transformers/all-MiniLM-L6-v2", help="Embedding model used for FAISS queries")
    parser.add_argument("--manifest", help="Optional chunk manifest JSON from ingestion (avoids re-splitting)")
    parser.add_argument("--gen_model", default="gemini-2.5-flash-lite", help="Generator model id (HF or gemini-*)")
    parser.add_argument("--max_new_tokens", type=int, default=200, help="Max tokens to generate")
    parser.add_argument("--num_beams", type=int, default=4, help="Beam search width to reduce repetition")
    return parser


def load_generator(model_id: str, num_beams: int, max_new_tokens: int):
    """Create a generation pipeline. Uses Gemini if model_id starts with 'gemini', otherwise HF."""
    # Load environment variables from .env if present.
    load_dotenv()
    if model_id.startswith("gemini"):
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("google-generativeai is required for gemini models. pip install google-generativeai")
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError("Set GOOGLE_API_KEY to use gemini models.")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_id)

        def run(prompt: str):
            resp = model.generate_content(prompt, generation_config={"max_output_tokens": max_new_tokens})
            return resp.text or ""

        return run

    # HF path
    cfg = AutoConfig.from_pretrained(model_id)
    task = "text2text-generation" if cfg.is_encoder_decoder else "text-generation"
    tok = AutoTokenizer.from_pretrained(model_id)
    pad_id = tok.eos_token_id
    pipeline_kwargs = {
        "task": task,
        "model": model_id,
        "tokenizer": tok,
        "truncation": True,
        "pad_token_id": pad_id,
    }
    if task == "text-generation":
        pipeline_kwargs["return_full_text"] = False
    generator = pipeline(**pipeline_kwargs)

    def run(prompt: str):
        gen_kwargs = {
            "max_new_tokens": max_new_tokens,
            "no_repeat_ngram_size": 4,
            "repetition_penalty": 1.2,
            "num_beams": num_beams if task == "text2text-generation" else None,
        }
        # Remove None to avoid warnings
        gen_kwargs = {k: v for k, v in gen_kwargs.items() if v is not None}
        out = generator(prompt, **gen_kwargs)[0]
        return out.get("generated_text") or out.get("text") or ""

    return run


def build_prompt(question: str, contexts: List[str], chunk_ids: List[str]) -> str:
    context_block = "\n\n".join([f"[{cid}] {text}" for cid, text in zip(chunk_ids, contexts)])
    return (
        "You are an conversational assistant. Answer in clear, conversational sentence that restates the subject and the answer (e.g., 'The undergraduate application deadline is Dec. 1.'). "
        "Use your own words, keep it natural, and avoid copying tables or lists. Return ONLY the sentence. "
        "Cite chunk ids inline in brackets at the very end of your answer (e.g., [admissions.md-0-chunk-00002]). "
        "If the answer is not in the context, you must say you do not have that information.\n\n"
        f"Question: {question}\n\n"
        f"Context:\n{context_block}\n\n"
        "Answer:"
    )

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
