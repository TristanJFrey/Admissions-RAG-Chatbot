import os
import sys
import argparse
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def main():
    """CLI arguments:
    --index: directory containing the saved FAISS index.
    --q: question to run against the index.
    --k: number of top matches to display.
    --model: embedding model used to reconstruct query vectors.

    Example:
    python src/query_faiss.py --index indexes/faiss_admissions --q "When is the undergrad application deadline?" --k 5
    """
    parser = argparse.ArgumentParser(description="Query FAISS index.")
    parser.add_argument("--index", required=True, help="Path to FAISS index directory")
    parser.add_argument("--q", required=True, help="Query text")
    parser.add_argument("--k", type=int, default=5, help="Top-k results")
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    args = parser.parse_args()

    # Recreate the embedding model so queries live in the same vector space as stored chunks.
    embeddings = HuggingFaceEmbeddings(model_name=args.model)
    # Load the persisted FAISS index (vectors + metadata stored on disk).
    vs = FAISS.load_local(args.index, embeddings, allow_dangerous_deserialization=True)
    # Perform similarity search to retrieve the closest chunks to the query.
    results = vs.similarity_search_with_score(args.q, k=args.k)

    for rank, (doc, score) in enumerate(results, start=1):
        meta = doc.metadata
        print(f"\n=== Result #{rank} ===")
        print(f"source   : {meta.get('source')}")
        print(f"chunk_id : {meta.get('chunk_id')}")
        print(f"score    : {score:.4f}")
        print(f"text     : {_preview_text(doc.page_content.strip())}")
        #print(f"text     : {_preview_text(d.page_content[:500].strip())}...") # makes it shorter


def _preview_text(text: str) -> str:
    """Clamp output to the active terminal encoding to avoid Windows cp1252 crashes."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    return text.encode(encoding, errors="replace").decode(encoding, errors="replace")

if __name__ == "__main__":
    main()
