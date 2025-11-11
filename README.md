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
