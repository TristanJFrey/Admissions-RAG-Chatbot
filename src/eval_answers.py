"""
Evaluate answer quality for dense-only vs hybrid RAG.

For each question:
- Retrieve with FAISS-only and with Hybrid (FAISS+BM25+RRF)
- Generate answers with a HF text2text model
- Score answers against gold reference text(s) using BERTScore (F1). References come from
  `answer` and `answer_short` if provided, otherwise the gold chunk text; the best (max) F1
  across provided references is used.
- Flag simple citation hallucinations (citations missing or pointing to unretrieved chunks)

Usage:
  python src/eval_answers.py --index indexes/faiss_admissions --doc data/admissions.md --manifest indexes/faiss_admissions/chunk_manifest.json --questions data/sample_questions.json --k 3 --faiss_k 8 --bm25_k 8 --max_new_tokens 128 --report_details
"""

import argparse
import json
import os
import re
import io
import contextlib
from typing import Dict, List, Tuple

from bert_score import score as bert_score

from answer_hybrid_rag import build_prompt, load_generator
from query_hybrid_rrf import (
    load_faiss_hits,
    load_bm25_hits,
    reciprocal_rank_fusion,
)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Answer-level eval: FAISS vs Hybrid RAG using BERTScore.")
    parser.add_argument("--index", required=True, help="Path to FAISS index directory")
    parser.add_argument("--doc", required=True, help="Path to DOCX source used for BM25 retrieval")
    parser.add_argument("--manifest", help="Optional chunk manifest JSON from ingestion (avoids re-splitting)")
    parser.add_argument("--questions", default="data/sample_questions.json", help="JSON with tests [{id,question,chunk_id}] or {'tests': [...]}")
    parser.add_argument("--k", type=int, default=3, help="Number of fused chunks to feed generator")
    parser.add_argument("--faiss_k", type=int, default=8, help="FAISS hits to fetch before fusion")
    parser.add_argument("--bm25_k", type=int, default=8, help="BM25 hits to fetch before fusion")
    parser.add_argument("--rrf_k", type=int, default=60, help="RRF k constant")
    parser.add_argument("--chunk_size", type=int, default=1200, help="Chunk size for BM25 splitter (match ingest)")
    parser.add_argument("--chunk_overlap", type=int, default=200, help="Chunk overlap for BM25 splitter (match ingest)")
    parser.add_argument("--embedding_model", default="sentence-transformers/all-MiniLM-L6-v2", help="Embedding model used for FAISS queries")
    parser.add_argument("--gen_model", default="gemini-2.5-flash-lite", help="Generator model id (HF or gemini-*)")
    parser.add_argument("--max_new_tokens", type=int, default=128, help="Max tokens to generate")
    parser.add_argument("--num_beams", type=int, default=4, help="Beam search width to reduce repetition")
    parser.add_argument("--report_details", action="store_true", help="Print per-question scores and hallucination flags")
    parser.add_argument("--report_answers", action="store_true", help="Print generated answers for FAISS and Hybrid")
    parser.add_argument("--out", help="Optional path to write the report text to a file")
    return parser


def load_questions(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, dict) and "tests" in payload:
        return payload["tests"]
    if isinstance(payload, list):
        return payload
    raise ValueError("Questions file must be a list or contain a 'tests' list.")


def load_manifest_chunks(manifest_path: str) -> Dict[str, str]:
    if not manifest_path or not os.path.exists(manifest_path):
        return {}
    with open(manifest_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    out = {}
    for entry in payload.get("chunks", []):
        cid = entry.get("chunk_id")
        text = entry.get("text", "")
        if cid and text:
            out[cid] = text
    return out


def citations_from_answer(answer: str) -> List[str]:
    return re.findall(r"\[([^\[\]]+)\]", answer)


def has_hallucinated_citation(answer: str, allowed_chunk_ids: List[str], gold_chunk_id: str) -> bool:
    cited = citations_from_answer(answer)
    if not cited:
        return True
    allowed = set(allowed_chunk_ids)
    # Any citation outside retrieved set
    if any(c not in allowed for c in cited):
        return True
    # If gold chunk id exists but was not cited
    if gold_chunk_id and gold_chunk_id not in cited:
        return True
    return False


def bertscore_f1(hypothesis: str, reference: str) -> float:
    _, _, f1 = bert_score([hypothesis], [reference], lang="en", verbose=False)
    return float(f1[0])


def bertscore_best_f1(hypothesis: str, references: List[str]) -> float:
    refs = [r for r in references if r and r.strip()]
    if not refs:
        return 0.0
    scores = [bertscore_f1(hypothesis, r) for r in refs]
    return max(scores) if scores else 0.0


def run_generation(
    question: str,
    fused_hits,
    generator,
) -> Tuple[str, List[str], List[str]]:
    top_docs = fused_hits
    contexts = [entry["doc"].page_content.strip() for entry in top_docs]
    chunk_ids = [entry["doc"].metadata.get("chunk_id", f"chunk-{i}") for i, entry in enumerate(top_docs)]
    prompt = build_prompt(question, contexts, chunk_ids)
    raw_answer = generator(prompt)
    answer = raw_answer.split("Sources:")[0].strip()
    return answer, contexts, chunk_ids


def evaluate(args):
    manifest_path = args.manifest
    if not manifest_path:
        candidate = os.path.join(args.index, "chunk_manifest.json")
        manifest_path = candidate if os.path.exists(candidate) else None

    gold_chunks = load_manifest_chunks(manifest_path)
    tests = load_questions(args.questions)

    generator = load_generator(args.gen_model, args.num_beams, args.max_new_tokens)

    records = []
    for entry in tests:
        qid = entry.get("id")
        question = entry["question"]
        gold_chunk_id = entry["chunk_id"]
        references = []
        if entry.get("answer"):
            references.append(entry["answer"])
        if entry.get("answer_short"):
            references.append(entry["answer_short"])
        chunk_text = gold_chunks.get(gold_chunk_id, "")
        if chunk_text:
            references.append(chunk_text)
        gold_answer = entry.get("answer") or entry.get("answer_short") or ""

        faiss_hits = load_faiss_hits(args.index, question, args.embedding_model, args.faiss_k)
        bm25_hits = load_bm25_hits(args.doc, question, args.bm25_k, args.chunk_size, args.chunk_overlap, manifest_path=manifest_path)

        fused_hybrid = reciprocal_rank_fusion(faiss_hits, bm25_hits, args.rrf_k, args.k)
        fused_faiss_only = [{"doc": d, "retrievals": {"faiss": {"rank": r + 1}}} for r, (d, _) in enumerate(faiss_hits[: args.k])]

        # Hybrid answer
        hyb_answer, hyb_contexts, hyb_chunk_ids = run_generation(question, fused_hybrid, generator)
        hyb_f1 = bertscore_best_f1(hyb_answer, references)
        hyb_hallucinated = has_hallucinated_citation(hyb_answer, hyb_chunk_ids, gold_chunk_id)

        # FAISS-only answer
        faiss_answer, faiss_contexts, faiss_chunk_ids = run_generation(question, fused_faiss_only, generator)
        faiss_f1 = bertscore_best_f1(faiss_answer, references)
        faiss_hallucinated = has_hallucinated_citation(faiss_answer, faiss_chunk_ids, gold_chunk_id)

        records.append(
            {
                "id": qid,
                "question": question,
                "gold_chunk": gold_chunk_id,
                "gold_answer": gold_answer,
                "hybrid_answer": hyb_answer,
                "faiss_answer": faiss_answer,
                "hybrid_f1": hyb_f1,
                "faiss_f1": faiss_f1,
                "hybrid_hallucinated": hyb_hallucinated,
                "faiss_hallucinated": faiss_hallucinated,
            }
        )

    return records


def summarize(records: List[Dict], show_details: bool):
    hyb_f1s = [r["hybrid_f1"] for r in records]
    faiss_f1s = [r["faiss_f1"] for r in records]
    hyb_hall = sum(1 for r in records if r["hybrid_hallucinated"])
    faiss_hall = sum(1 for r in records if r["faiss_hallucinated"])
    total = len(records)

    print("\n=== Answer-Level Evaluation ===")
    print(f"Questions        : {total}")
    print(f"Hybrid BERTScore : mean F1 {sum(hyb_f1s)/total:.4f}")
    print(f"FAISS  BERTScore : mean F1 {sum(faiss_f1s)/total:.4f}")
    print(f"Hybrid hallucinations (citation missing/out-of-pool): {hyb_hall}/{total}")
    print(f"FAISS hallucinations (citation missing/out-of-pool): {faiss_hall}/{total}")

    if show_details:
        print("\nID | Hybrid F1 | FAISS F1 | Hybrid Hall? | FAISS Hall?")
        for r in sorted(records, key=lambda x: x["id"]):
            print(
                f"{r['id']:>2} | {r['hybrid_f1']:.4f} | {r['faiss_f1']:.4f} | "
                f"{'Y' if r['hybrid_hallucinated'] else 'N'} | {'Y' if r['faiss_hallucinated'] else 'N'}"
            )


def report_answers(records: List[Dict]):
    print("\n=== Generated Answers ===")
    for r in sorted(records, key=lambda x: x["id"]):
        print(f"\nQ{r['id']}: {r['question']}")
        print(f"Gold chunk : {r['gold_chunk']}")
        if r.get("gold_answer"):
            print(f"Gold answer: {r['gold_answer']}")
        print(f"FAISS ans  : {r['faiss_answer']}")
        print(f"Hybrid ans : {r['hybrid_answer']}")


def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    records = evaluate(args)
    # Print to console
    summarize(records, args.report_details)
    if args.report_answers:
        report_answers(records)
    # Optionally write report to file
    if args.out:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            summarize(records, args.report_details)
            if args.report_answers:
                report_answers(records)
        out_text = buf.getvalue()
        out_path = os.path.abspath(args.out)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out_text)
        print(f"\nReport written to {out_path}")


if __name__ == "__main__":
    main()
