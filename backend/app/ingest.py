import os
from typing import List, Dict, Any
from pypdf import PdfReader
from docx import Document
from .utils import iter_files, chunk_text
from .rag import build_or_update_index

DOCS_PATH = os.getenv("DOCS_PATH", "data/docs")

def load_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    elif ext == ".docx":
        return "\n".join(p.text for p in Document(path).paragraphs)
    elif ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return ""

def make_chunks(docs_path: str, chunk_size: int, chunk_overlap: int) -> List[Dict[str, Any]]:
    chunks = []
    for fpath in iter_files(docs_path):
        text = load_text_from_file(fpath)
        for i, part in enumerate(chunk_text(text, chunk_size, chunk_overlap)):
            chunks.append({"source": os.path.relpath(fpath, start=docs_path),
                           "chunk_id": i, "text": part})
    return chunks

def ingest(docs_path: str = None, chunk_size=800, chunk_overlap=200):
    if docs_path is None: docs_path = DOCS_PATH
    chunks = make_chunks(docs_path, chunk_size, chunk_overlap)
    if not chunks: return {"status": "no_files", "message": f"No docs in {docs_path}"}
    build_or_update_index(chunks)
    return {"status": "ok", "chunks": len(chunks)}
