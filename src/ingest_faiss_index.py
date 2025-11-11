import os
import argparse
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def main():
    """CLI arguments:
    --doc: path to the DOCX admissions file to ingest.
    --out: directory where the FAISS index will be written.
    --chunk_size: maximum characters per chunk before embedding (default 1200).
    --chunk_overlap: shared characters between adjacent chunks (default 200).
    --model: Hugging Face sentence-transformer used for embeddings.
    """
    parser = argparse.ArgumentParser(description="Ingest DOCX -> chunks -> FAISS (free embeddings).")
    parser.add_argument("--doc", required=True, help="Path to .docx file")
    parser.add_argument("--out", required=True, help="Output dir for FAISS index")
    parser.add_argument("--chunk_size", type=int, default=1200)
    parser.add_argument("--chunk_overlap", type=int, default=200)
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    args = parser.parse_args()

    # Error handle for Path/File
    if not os.path.exists(args.doc):
        raise FileNotFoundError(f"Document not found: {args.doc}")

    # Load DOCX into LangChain Document objects (one per paragraph by default).
    docs = Docx2txtLoader(args.doc).load()
    for i, d in enumerate(docs):
        d.metadata.update({"source": os.path.basename(args.doc), "doc_id": f"{os.path.basename(args.doc)}-{i}"})

    # Chunk long documents so FAISS receives manageable, overlapping text windows.
    splitter = RecursiveCharacterTextSplitter(chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap, separators=["\n\n","\n"," ",""])
    chunks = splitter.split_documents(docs)
    for i, c in enumerate(chunks):
        c.metadata["chunk_id"] = f"{c.metadata['doc_id']}-chunk-{i:05d}"

    # Embed chunks with a sentence-transformer model and build a FAISS index from them.
    embeddings = HuggingFaceEmbeddings(model_name=args.model)
    vs = FAISS.from_documents(chunks, embeddings)
    # Persist FAISS index (faiss + metadata files) so it can be queried later.
    os.makedirs(args.out, exist_ok=True)
    vs.save_local(args.out)
    print(f"Saved FAISS index -> {args.out}")

if __name__ == "__main__":
    main()
