"""
Compare FAISS-only retrieval vs hybrid Reciprocal Rank Fusion (FAISS+BM25)
on the questions listed in data/sample_questions.json (or another JSON file
with the same schema).

For each question we check whether the top-ranked chunk matches the ground-truth
chunk that contains the relevant policy text. Ground truth is derived by
matching distinctive substrings inside the admissions document.

Example:
    python src/eval_retrievers.py --index indexes/faiss_admissions --doc data/admissions.docx --questions data/sample_questions.json
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

from query_hybrid_rrf import (
    load_bm25_hits,
    load_faiss_hits,
    reciprocal_rank_fusion,
)


@dataclass
class EvalRecord:
    question_id: int
    question: str
    gold_chunk: str
    faiss_top: Optional[str]
    rrf_top: Optional[str]
    faiss_chunks: List[str]
    rrf_chunks: List[str]

    @property
    def faiss_correct(self) -> bool:
        return self.faiss_top == self.gold_chunk

    @property
    def rrf_correct(self) -> bool:
        return self.rrf_top == self.gold_chunk

    def faiss_hit_within(self, k: int) -> bool:
        return self.gold_chunk in self.faiss_chunks[:k]

    def rrf_hit_within(self, k: int) -> bool:
        return self.gold_chunk in self.rrf_chunks[:k]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate FAISS vs hybrid RRF retrieval accuracy.")
    parser.add_argument("--index", required=True, help="Path to FAISS index directory")
    parser.add_argument("--doc", required=True, help="Path to the admissions DOCX file")
    parser.add_argument(
        "--questions",
        default="data/sample_questions.json",
        help="JSON file with 'tests': [{id, question, chunk_id}]",
    )
    parser.add_argument("--faiss_k", type=int, default=5, help="FAISS hits to consider")
    parser.add_argument("--bm25_k", type=int, default=5, help="BM25 hits to consider")
    parser.add_argument("--rrf_k", type=int, default=60, help="RRF k constant")
    parser.add_argument("--chunk_size", type=int, default=1200, help="Chunk size (match ingest)")
    parser.add_argument("--chunk_overlap", type=int, default=200, help="Chunk overlap (match ingest)")
    parser.add_argument("--embedding_model", default="sentence-transformers/all-MiniLM-L6-v2", help="Embedding model used when building the FAISS index")
    parser.add_argument("--show_details", action="store_true", help="Print per-question debug info")
    parser.add_argument("--report_k", type=int, default=3, help="Report hit rates up to this rank (e.g. 3 => top-1/2/3)")
    return parser


def load_questions(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, dict) and "tests" in payload:
        data = payload["tests"]
    elif isinstance(payload, list):
        data = payload
    else:
        raise ValueError("Questions file must be a list or contain a 'tests' list.")
    for entry in data:
        if "chunk_id" not in entry:
            raise KeyError(f"Question id={entry.get('id')} missing 'chunk_id' field.")
    return data


def evaluate(args) -> List[EvalRecord]:
    results: List[EvalRecord] = []

    questions = load_questions(args.questions)
    report_k = max(1, args.report_k)
    faiss_fetch = max(args.faiss_k, report_k)
    rrf_fetch = report_k

    for entry in questions:
        qid = int(entry["id"])
        question = entry["question"]
        gold_chunk_id = entry["chunk_id"]

        faiss_hits = load_faiss_hits(args.index, question, args.embedding_model, faiss_fetch)
        bm25_hits = load_bm25_hits(args.doc, question, args.bm25_k, args.chunk_size, args.chunk_overlap)
        fused = reciprocal_rank_fusion(faiss_hits, bm25_hits, args.rrf_k, final_k=rrf_fetch)

        faiss_top = faiss_hits[0][0].metadata.get("chunk_id") if faiss_hits else None
        rrf_top = fused[0]["doc"].metadata.get("chunk_id") if fused else None
        faiss_chunks = [hit[0].metadata.get("chunk_id") for hit in faiss_hits]
        rrf_chunks = [entry["doc"].metadata.get("chunk_id") for entry in fused]

        results.append(
            EvalRecord(
                question_id=qid,
                question=question,
                gold_chunk=gold_chunk_id,
                faiss_top=faiss_top,
                rrf_top=rrf_top,
                faiss_chunks=faiss_chunks,
                rrf_chunks=rrf_chunks,
            )
        )
    return results


def main():
    args = build_arg_parser().parse_args()
    records = evaluate(args)
    total = len(records)
    faiss_correct = sum(1 for r in records if r.faiss_correct)
    rrf_correct = sum(1 for r in records if r.rrf_correct)

    if args.show_details:
        print("\nQuestion ID | Gold Chunk | FAISS Top | RRF Top | Notes")
        for rec in sorted(records, key=lambda r: r.question_id):
            faiss_status = "OK " if rec.faiss_correct else "MISS"
            rrf_status = "OK " if rec.rrf_correct else "MISS"
            print(
                f"{rec.question_id:>11} | {rec.gold_chunk} | "
                f"{rec.faiss_top or 'n/a':<25} ({faiss_status}) | "
                f"{rec.rrf_top or 'n/a':<25} ({rrf_status})"
            )

    print("\n=== Evaluation Summary ===")
    print(f"Questions evaluated : {total}")

    for k in range(1, args.report_k + 1):
        faiss_hits_k = sum(1 for r in records if r.faiss_hit_within(k))
        rrf_hits_k = sum(1 for r in records if r.rrf_hit_within(k))
        print(f"FAISS top-{k} hits : {faiss_hits_k}/{total}")
        print(f"RRF top-{k} hits   : {rrf_hits_k}/{total}")


if __name__ == "__main__":
    main()
