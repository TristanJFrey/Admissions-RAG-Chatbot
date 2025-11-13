# Admissions-RAG-Chatbot

## 1. Environment Setup

```powershell
python -m venv .venv           # create virtual env once
.\.venv\Scripts\Activate.ps1   # activate
python -m pip install -r requirements.txt
```

## 2. Build the FAISS Index

Point `--doc` at your admissions source file and choose an output folder for the index.

```powershell
python src/ingest_faiss_index.py --doc data/admissions.docx --out indexes/faiss_admissions
```

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
```

Example:

```powershell
python src/query_bm25.py --doc data/admissions.docx --q "When is the undergrad application deadline?" --k 5
```

## 5. Hybrid search with Reciprocal Rank Fusion (RRF)

Run FAISS (dense) and BM25 (lexical) together, then fuse the rankings so highly ranked chunks from either retriever bubble up.

General form:

```powershell
python src/query_hybrid_rrf.py --index <path_to_faiss_index> --doc <path_to_input_document> --q "<your question>" --k <final_results> --faiss_k <faiss_hits> --bm25_k <bm25_hits>
```

Example:

```powershell
python src/query_hybrid_rrf.py --index indexes/faiss_admissions --doc data/admissions.docx --q "When is the undergrad application deadline?" --k 5 --faiss_k 10 --bm25_k 10
```

## 6. Evaluate FAISS vs Hybrid RRF

Count how many sample questions are answered with the correct chunk by FAISS-only retrieval versus the hybrid RRF pipeline.

```powershell
python src/eval_retrievers.py --index indexes/faiss_admissions --doc data/admissions.docx --questions data/sample_questions.json --show_details --report_k 3
```

`--show_details` prints the gold chunk id along with the top chunk for each retriever so you can inspect misses.
Use `--report_k` to control how many ranks you want to track (top-1/2/3 accuracy by default).
