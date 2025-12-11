import argparse
import json
import os
from typing import List, Dict, Any
from langchain_community.document_loaders import Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import copy

def main():
    """Ingest DOCX or Markdown -> chunks -> FAISS index + chunk manifest (shared by all retrievers).
    CLI arguments:
    --doc: path to the admissions file to ingest (.docx or .md/.txt).
    --out: directory where the index + manifest will be written.
    --chunk_size: maximum characters per chunk before embedding (default 1200).
    --chunk_overlap: shared characters between adjacent chunks (default 200).
    --model: Hugging Face sentence-transformer used for embeddings.
    """
    parser = argparse.ArgumentParser(description="Ingest DOCX/Markdown -> chunks -> FAISS index + manifest (free embeddings).")
    parser.add_argument("--doc", required=True, help="Path to .docx file")
    parser.add_argument("--out", required=True, help="Output dir for FAISS index")
    parser.add_argument("--chunk_size", type=int, default=1200)
    parser.add_argument("--chunk_overlap", type=int, default=200)
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--dump_chunks", help="Optional directory to write one .txt file per chunk")
    args = parser.parse_args()

    # Error handle for Path/File
    if not os.path.exists(args.doc):
        raise FileNotFoundError(f"Document not found: {args.doc}")

    # Load DOCX or Markdown into LangChain Document objects.
    ext = os.path.splitext(args.doc)[1].lower()
    if ext == ".docx":
        docs = Docx2txtLoader(args.doc).load()
        for i, d in enumerate(docs):
            d.metadata.update({"source": os.path.basename(args.doc), "doc_id": f"{os.path.basename(args.doc)}-{i}"})
        # First pass: break on paragraph-ish boundaries and carry forward headings to keep semantic chunks together.
        section_docs = _segment_with_headings(docs)
    else:
        # Treat as markdown/plain text; split by headings first to respect sections.
        docs = TextLoader(args.doc, encoding="utf-8").load()
        section_docs = _segment_markdown_by_headers(docs, source_name=os.path.basename(args.doc))

    if ext != ".docx":
        # For markdown, keep section chunks as-is to avoid fragmenting tables/sections.
        chunks = []
        for i, c in enumerate(section_docs):
            c.metadata["chunk_id"] = f"{c.metadata['doc_id']}-chunk-{i:05d}"
            chunks.append(c)
    else:
        # Second pass: apply character splitter for long sections.
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )
        chunks = splitter.split_documents(section_docs)
        for i, c in enumerate(chunks):
            c.metadata["chunk_id"] = f"{c.metadata['doc_id']}-chunk-{i:05d}"

    # Embed chunks with a sentence-transformer model and build a FAISS index from them.
    embeddings = HuggingFaceEmbeddings(model_name=args.model)
    vs = FAISS.from_documents(chunks, embeddings)
    # Persist FAISS index (faiss + metadata files) so it can be queried later.
    os.makedirs(args.out, exist_ok=True)
    vs.save_local(args.out)
    manifest_path = os.path.join(args.out, "chunk_manifest.json")
    _write_chunk_manifest(manifest_path, chunks, args)
    print(f"Saved FAISS index -> {args.out}")
    print(f"Wrote chunk manifest -> {manifest_path}")
    if args.dump_chunks:
        dump_dir = os.path.abspath(args.dump_chunks)
        _dump_chunks_to_txt(chunks, dump_dir)
        print(f"Wrote chunk text files -> {dump_dir}")


def _write_chunk_manifest(path: str, chunks: List[Document], args: argparse.Namespace) -> None:
    manifest: Dict[str, Any] = {
        "document": {
            "path": os.path.abspath(args.doc),
            "name": os.path.basename(args.doc),
        },
        "ingestion": {
            "chunk_size": args.chunk_size,
            "chunk_overlap": args.chunk_overlap,
            "embedding_model": args.model,
            "num_chunks": len(chunks),
        },
        "chunks": [],
    }
    for idx, chunk in enumerate(chunks):
        manifest["chunks"].append(
            {
                "ordinal": idx,
                "chunk_id": chunk.metadata.get("chunk_id"),
                "doc_id": chunk.metadata.get("doc_id"),
                "source": chunk.metadata.get("source"),
                "text": chunk.page_content,
            }
        )
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def _segment_with_headings(docs: List[Document]) -> List[Document]:
    """Heuristic segmentation: detect short heading lines and prepend them to following blocks."""
    out: List[Document] = []

    def is_heading(text: str) -> bool:
        t = text.strip()
        if not t:
            return False
        word_count = len(t.split())
        return len(t) <= 80 and word_count <= 12

    for d in docs:
        parts = [p.strip() for p in d.page_content.split("\n\n") if p.strip()]
        current_heading = ""
        for part in parts:
            if is_heading(part):
                current_heading = part
                continue
            new_text = part
            if current_heading:
                new_text = f"{current_heading}\n\n{part}"
            nd = copy.deepcopy(d)
            nd.page_content = new_text
            out.append(nd)
    return out


def _segment_markdown_by_headers(docs: List[Document], source_name: str) -> List[Document]:
    """Split markdown using headers so each section stays together."""
    if not docs:
        return []
    md_text = "\n\n".join(d.page_content for d in docs)
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
            ("####", "h4"),
        ],
        strip_headers=False,
    )
    sections = splitter.split_text(md_text)
    out: List[Document] = []
    for idx, sec in enumerate(sections):
        headers = sec.metadata.get("headers", [])
        section_path = " > ".join([h for _, h in headers if h])
        meta = {
            "source": source_name,
            "doc_id": f"{source_name}-{idx}",
            "section_path": section_path,
        }
        out.append(Document(page_content=sec.page_content, metadata=meta))
    if not out:
        # fallback: return the raw text as one doc
        out.append(Document(page_content=md_text, metadata={"source": source_name, "doc_id": f"{source_name}-0"}))
    return out


def _dump_chunks_to_txt(chunks: List[Document], out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    for chunk in chunks:
        cid = chunk.metadata.get("chunk_id", "chunk")
        safe_name = cid.replace("/", "_")
        out_path = os.path.join(out_dir, f"{safe_name}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(chunk.page_content)

if __name__ == "__main__":
    main()
