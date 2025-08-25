import os, json, numpy as np, faiss
from typing import List, Dict, Any, Tuple
from .llm import embed_texts, generate_answer

INDEX_PATH = os.getenv("INDEX_PATH", "data/index/index.faiss")
META_PATH = os.getenv("META_PATH", "data/index/meta.json")

SYSTEM_PROMPT = ("You are a careful assistant. "
                 "Answer ONLY from the provided context. "
                 "If not found, say you don't know.")

def _normalize(a): faiss.normalize_L2(a); return a

def load_index():
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r", encoding="utf-8") as f: meta = json.load(f)
    return index, meta

def save_index(index, meta):
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w", encoding="utf-8") as f: json.dump(meta, f, indent=2)

def build_or_update_index(chunks):
    texts = [c["text"] for c in chunks]
    vecs = np.array(embed_texts(texts), dtype="float32")
    _normalize(vecs)
    index = faiss.IndexFlatIP(vecs.shape[1])
    index.add(vecs)
    save_index(index, chunks)

def search(query: str, k=4):
    index, meta = load_index()
    qvec = _normalize(np.array(embed_texts([query])[0], dtype="float32").reshape(1, -1))
    D, I = index.search(qvec, k)
    return I[0].tolist(), D[0].tolist(), meta

def answer_question(question: str, k=4):
    idxs, scores, meta = search(question, k)
    context = "\n\n".join(f"[{i}] {meta[j]['text']} (source: {meta[j]['source']})"
                          for i, j in enumerate(idxs, 1))
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer concisely."
    ans = generate_answer(prompt, system=SYSTEM_PROMPT)
    return {"answer": ans, "sources": [meta[j] for j in idxs], "scores": scores}
