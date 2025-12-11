# Admissions-RAG-Chatbot

## 1. Environment Setup

```powershell
python -m venv .venv           # create virtual env once
.\.venv\Scripts\Activate.ps1   # activate
python -m pip install -r requirements.txt
```

## 2. Build the FAISS Index

Convert the DOCX to Markdown (keeps tables/structure), then point `--doc` at the Markdown file and choose an output folder for the index.

```powershell
python scripts/convert_docx_to_md.py data/admissions.docx data/admissions.md
python src/ingest_corpus.py --doc data/admissions.md --out indexes/faiss_admissions
```

This writes both the FAISS index and a `chunk_manifest.json` in the output directory so downstream BM25/Hybrid/Eval runs reuse the exact same chunks (no re-splitting drift).

## 3. Query the Index

General form:

```powershell
python src/query_faiss.py --index <path_to_faiss_index> --q "<your question>" --k <top_k_results>
```

Example:

```powershell
python src/query_faiss.py --index indexes/faiss_admissions --q "When is the undergrad application deadline?" --k 5
```

## 4. Query the corpus using BM25

Current implementation only handles a single document.

General form:

```powershell
python src/query_bm25.py --doc <path_to_input_document> --q "<your question>" --k <top_k_results>
# or reuse the manifest emitted at ingest time (recommended)
python src/query_bm25.py --doc data/admissions.md --manifest indexes/faiss_admissions/chunk_manifest.json --q "When is the undergrad application deadline?" --k 5
```

Example:

```powershell
python src/query_bm25.py --doc data/admissions.md --q "When is the undergrad application deadline?" --k 5
```

## 5. Hybrid search with Reciprocal Rank Fusion (RRF)

Run FAISS (dense) and BM25 (lexical) together, then fuse the rankings so highly ranked chunks from either retriever bubble up.

General form:

```powershell
python src/query_hybrid_rrf.py --index <path_to_faiss_index> --doc <path_to_input_document> --q "<your question>" --k <final_results> --faiss_k <faiss_hits> --bm25_k <bm25_hits>
# recommended: point BM25 at the manifest so chunk ids stay aligned
python src/query_hybrid_rrf.py --index indexes/faiss_admissions --doc data/admissions.md --manifest indexes/faiss_admissions/chunk_manifest.json --q "When is the undergrad application deadline?" --k 5 --faiss_k 10 --bm25_k 10
```

Example:

```powershell
python src/query_hybrid_rrf.py --index indexes/faiss_admissions --doc data/admissions.md --q "When is the undergrad application deadline?" --k 5 --faiss_k 10 --bm25_k 10
```

## 6. Evaluate FAISS vs Hybrid RRF

Count how many sample questions are answered with the correct chunk by FAISS-only retrieval versus the hybrid RRF pipeline.

```powershell
python src/eval_retrievers.py --index indexes/faiss_admissions --doc data/admissions.md --manifest indexes/faiss_admissions/chunk_manifest.json --questions data/sample_questions.json --show_details --report_k 3
```

`--show_details` prints the gold chunk id along with the top chunk for each retriever so you can inspect misses.
Use `--report_k` to control how many ranks you want to track (top-1/2/3 accuracy by default).

## 7. Generate Answers (Hybrid RAG)

Run hybrid retrieval, then generate an answer with citations using a Hugging Face text2text model (default: `google/flan-t5-base`):

```powershell
python src/answer_hybrid_rag.py --index indexes/faiss_admissions --doc data/admissions.md --manifest indexes/faiss_admissions/chunk_manifest.json --q "When is the undergrad application deadline?" --k 4 --faiss_k 10 --bm25_k 10 --max_new_tokens 200
```

## 8. Evaluate Answers (BERTScore + hallucination check)

Compare FAISS-only vs Hybrid RAG answers against gold chunks using BERTScore and a simple citation hallucination flag:

```powershell
python src/eval_answers.py --index indexes/faiss_admissions --doc data/admissions.md --manifest indexes/faiss_admissions/chunk_manifest.json --questions data/sample_questions.json --k 3 --faiss_k 8 --bm25_k 8 --max_new_tokens 128 --report_details
```

Notes:
- If your questions file supplies `answer` and/or `answer_short`, the best BERTScore against those is used; otherwise the gold chunk text is used (which can deflate scores if answers are very short).
