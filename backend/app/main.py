from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from .ingest import ingest as ingest_pipeline
from .rag import answer_question

app = FastAPI(title="Local RAG Bot", version="1.0.0")

# Allow frontend (running separately) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ allow all for dev; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestReq(BaseModel):
    docs_path: Optional[str] = None
    chunk_size: Optional[int] = 800
    chunk_overlap: Optional[int] = 200

class QueryReq(BaseModel):
    question: str
    k: Optional[int] = 4

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(req: IngestReq):
    return ingest_pipeline(docs_path=req.docs_path,
                           chunk_size=req.chunk_size or 800,
                           chunk_overlap=req.chunk_overlap or 200)

@app.post("/query")
def query(req: QueryReq):
    return answer_question(req.question, k=req.k or 4)
