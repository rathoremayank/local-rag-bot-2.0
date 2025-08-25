import os, requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

def _post(path, payload):
    url = OLLAMA_URL.rstrip("/") + path
    r = requests.post(url, json=payload, timeout=120); r.raise_for_status()
    return r.json()

def embed_texts(texts):
    return [_post("/api/embeddings", {"model": EMBED_MODEL, "prompt": t})["embedding"] for t in texts]

def generate_answer(prompt, system=None):
    payload = {"model": LLM_MODEL, "prompt": prompt, "stream": False}
    if system: payload["system"] = system
    return _post("/api/generate", payload).get("response", "").strip()
