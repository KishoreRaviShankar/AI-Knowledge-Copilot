import os
import re
from pathlib import Path

import faiss
import numpy as np
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pypdf import PdfReader
from docx import Document as DocxDocument
from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi
from google import genai
from dotenv import load_dotenv


load_dotenv()

PROJECT_NAME = "AI Enterprise Knowledge Intelligence & Decision Copilot"
CHUNK_SIZE = 350
CHUNK_OVERLAP = 75
SEMANTIC_TOP_K = 12
KEYWORD_TOP_K = 12
FINAL_TOP_K = 5
SIMILARITY_THRESHOLD = 0.20
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
GEMINI_MODEL = "gemini-3.6-flash"

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "data"
UPLOAD_DIR.mkdir(exist_ok=True)

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title=PROJECT_NAME)

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)

print("BASE_DIR:", BASE_DIR)
print("TEMPLATES_DIR:", TEMPLATES_DIR)
print("index.html exists:", (TEMPLATES_DIR / "index.html").exists())

api_key = os.getenv("GEMINI_API_KEY", "").strip()

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

if "\n" in api_key or "\r" in api_key:
    raise ValueError("GEMINI_API_KEY contains an invalid line break")

client = genai.Client(api_key=api_key)


embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
reranker = CrossEncoder(RERANKER_MODEL_NAME)

documents = []
chunks = []
chunk_embeddings = None
faiss_index = None
bm25_index = None
conversation_history = []
knowledge_base_ready = False


def clean_text(text):
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    return text.strip()


def extract_pdf(file_path):
    results = []
    try:
        reader = PdfReader(file_path)
        for page_number, page in enumerate(reader.pages, start=1):
            text = clean_text(page.extract_text() or "")
            if text:
                results.append({
                    "text": text, "source": Path(file_path).name,
                    "page": page_number, "file_type": "PDF"
                })
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return results


def extract_docx(file_path):
    results = []
    try:
        document = DocxDocument(file_path)
        text = "\n".join(
            p.text.strip() for p in document.paragraphs if p.text.strip()
        )
        text = clean_text(text)
        if text:
            results.append({
                "text": text, "source": Path(file_path).name,
                "page": "N/A", "file_type": "DOCX"
            })
    except Exception as e:
        print(f"DOCX extraction error: {e}")
    return results


def extract_txt(file_path):
    results = []
    try:
        text = clean_text(Path(file_path).read_text(encoding="utf-8"))
        if text:
            results.append({
                "text": text, "source": Path(file_path).name,
                "page": "N/A", "file_type": "TXT"
            })
    except Exception as e:
        print(f"TXT extraction error: {e}")
    return results


def extract_document(file_path):
    extension = Path(file_path).suffix.lower()
    if extension == ".pdf":
        return extract_pdf(file_path)
    if extension == ".docx":
        return extract_docx(file_path)
    if extension == ".txt":
        return extract_txt(file_path)
    return []


def create_chunks(extracted_documents):
    all_chunks = []
    chunk_id = 0
    for document in extracted_documents:
        words = document["text"].split()
        start = 0
        while start < len(words):
            end = start + CHUNK_SIZE
            chunk_text = " ".join(words[start:end]).strip()
            if chunk_text:
                all_chunks.append({
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                    "source": document["source"],
                    "page": document["page"],
                    "file_type": document["file_type"]
                })
                chunk_id += 1
            next_start = end - CHUNK_OVERLAP
            if next_start <= start:
                break
            start = next_start
    return all_chunks


def build_knowledge_base():
    global documents, chunks, chunk_embeddings
    global faiss_index, bm25_index, knowledge_base_ready

    documents = []
    chunks = []
    chunk_embeddings = None
    faiss_index = None
    bm25_index = None
    knowledge_base_ready = False

    files = [
        file for file in UPLOAD_DIR.iterdir()
        if file.suffix.lower() in [".pdf", ".docx", ".txt"]
    ]

    if not files:
        return {"success": False, "message": "No documents found."}

    for file in files:
        documents.extend(extract_document(file))

    if not documents:
        return {"success": False, "message": "No readable documents found."}

    chunks = create_chunks(documents)
    if not chunks:
        return {"success": False, "message": "No chunks created."}

    texts = [chunk["text"] for chunk in chunks]
    chunk_embeddings = embedding_model.encode(
        texts, convert_to_numpy=True, normalize_embeddings=True
    ).astype("float32")

    faiss_index = faiss.IndexFlatIP(chunk_embeddings.shape[1])
    faiss_index.add(chunk_embeddings)

    bm25_index = BM25Okapi([text.lower().split() for text in texts])
    knowledge_base_ready = True

    return {
        "success": True,
        "documents": len({c["source"] for c in chunks}),
        "sections": len(documents),
        "chunks": len(chunks),
        "vectors": faiss_index.ntotal
    }


def semantic_search(question):
    if faiss_index is None:
        return []
    query_embedding = embedding_model.encode(
        [question], convert_to_numpy=True, normalize_embeddings=True
    ).astype("float32")
    scores, indices = faiss_index.search(query_embedding, SEMANTIC_TOP_K)
    return [
        {"index": int(idx), "semantic_score": float(score)}
        for score, idx in zip(scores[0], indices[0])
        if idx != -1 and score >= SIMILARITY_THRESHOLD
    ]


def keyword_search(question):
    if bm25_index is None:
        return []
    scores = bm25_index.get_scores(question.lower().split())
    indices = np.argsort(scores)[::-1][:KEYWORD_TOP_K]
    return [
        {"index": int(idx), "keyword_score": float(scores[idx])}
        for idx in indices if scores[idx] > 0
    ]


def hybrid_search(question):
    combined = {}
    for result in semantic_search(question):
        combined[result["index"]] = {
            "index": result["index"],
            "semantic_score": result["semantic_score"],
            "keyword_score": 0.0
        }
    for result in keyword_search(question):
        idx = result["index"]
        combined.setdefault(idx, {
            "index": idx, "semantic_score": 0.0, "keyword_score": 0.0
        })
        combined[idx]["keyword_score"] = result["keyword_score"]
    return list(combined.values())


def rerank_results(question, candidates):
    if not candidates:
        return []
    pairs = [[question, chunks[c["index"]]["text"]] for c in candidates]
    scores = reranker.predict(pairs)
    results = []
    for candidate, score in zip(candidates, scores):
        chunk = chunks[candidate["index"]].copy()
        chunk["rerank_score"] = float(score)
        chunk["semantic_score"] = candidate.get("semantic_score", 0)
        chunk["keyword_score"] = candidate.get("keyword_score", 0)
        results.append(chunk)
    results.sort(key=lambda x: x["rerank_score"], reverse=True)
    return results[:FINAL_TOP_K]


def retrieve(question):
    return rerank_results(question, hybrid_search(question))


def format_history():
    if not conversation_history:
        return "No previous conversation."
    return "\n".join(
        f"USER:\n{x['user']}\n\nASSISTANT:\n{x['assistant']}"
        for x in conversation_history
    )


def rewrite_query(question):
    prompt = f"""Convert the user's latest question into a standalone search query.
Use previous conversation only when needed.
Return only the rewritten query.

Conversation:
{format_history()}

Latest question:
{question}"""
    try:
        return client.models.generate_content(
            model=GEMINI_MODEL, contents=prompt
        ).text.strip()
    except Exception:
        return question


def build_context(question):
    retrieved = retrieve(question)
    if not retrieved:
        return "", []
    parts = []
    for i, chunk in enumerate(retrieved, start=1):
        parts.append(
            f"SOURCE {i}\nDocument: {chunk['source']}\n"
            f"Page: {chunk['page']}\nContent:\n{chunk['text']}"
        )
    return "\n\n".join(parts), retrieved


def generate_answer(question):
    global conversation_history

    if not knowledge_base_ready:
        return {"answer": "Please upload documents and build the knowledge base first.", "sources": []}
    if not question.strip():
        return {"answer": "Please enter a question.", "sources": []}

    search_query = rewrite_query(question)
    context, retrieved = build_context(search_query)

    if not context:
        answer = "I couldn't find sufficient information in the uploaded organizational documents."
        conversation_history.append({"user": question, "assistant": answer})
        return {"answer": answer, "sources": []}

    prompt = f"""You are an AI Enterprise Knowledge Intelligence and Decision Copilot.

Answer the user's question using ONLY the provided organizational context.
Do not invent information or use outside knowledge.
If unavailable, say:
"I couldn't find sufficient information in the uploaded organizational documents."
If multiple documents disagree, explain the difference.
Be professional and concise.

CONVERSATION:
{format_history()}

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:"""

    try:
        answer = client.models.generate_content(
            model=GEMINI_MODEL, contents=prompt
        ).text.strip()
    except Exception as e:
        return {"answer": f"Generation error: {e}", "sources": []}

    sources = [
        {
            "document": chunk["source"],
            "page": chunk["page"],
            "score": round(chunk["rerank_score"], 4)
        }
        for chunk in retrieved
    ]

    conversation_history.append({"user": question, "assistant": answer})
    if len(conversation_history) > 10:
        conversation_history.pop(0)

    return {"answer": answer, "sources": sources}


def summarize_document(document_name):
    selected = [c for c in chunks if c["source"] == document_name]
    if not selected:
        return "Document not found."

    text = "\n\n".join(c["text"] for c in selected)[:80000]

    prompt = f"""You are an enterprise document analyst.
Summarize this organizational document.

Document:
{document_name}

Content:
{text}

Return:
# Executive Summary
# Key Policies
# Important Rules
# Responsibilities
# Important Dates / Numbers
# Exceptions
# Action Items

Use ONLY the provided document."""

    try:
        return client.models.generate_content(
            model=GEMINI_MODEL, contents=prompt
        ).text.strip()
    except Exception as e:
        return f"Summary error: {e}"


def compare_documents(document_a, document_b):
    a = [c for c in chunks if c["source"] == document_a]
    b = [c for c in chunks if c["source"] == document_b]

    if not a or not b:
        return "Document not found."

    text_a = "\n\n".join(x["text"] for x in a)[:50000]
    text_b = "\n\n".join(x["text"] for x in b)[:50000]

    prompt = f"""Compare these organizational documents.

DOCUMENT A:
{document_a}
{text_a}

DOCUMENT B:
{document_b}
{text_b}

Return:
# Executive Summary
# Major Differences
| Topic | Document A | Document B |
# New Information
# Removed Information
# Changed Policies
# Business Impact
# Recommended Actions

Only identify differences supported by the documents."""

    try:
        return client.models.generate_content(
            model=GEMINI_MODEL, contents=prompt
        ).text.strip()
    except Exception as e:
        return f"Comparison error: {e}"


def decision_copilot(situation):
    if not knowledge_base_ready:
        return {"answer": "Please build the knowledge base first.", "sources": []}

    context, retrieved = build_context(situation)
    if not context:
        return {
            "answer": "I couldn't find sufficient organizational information to support this decision.",
            "sources": []
        }

    prompt = f"""You are an Enterprise Decision Copilot.

Analyze the situation using ONLY the organizational documents.

Situation:
{situation}

Context:
{context}

Return:
# Decision
# Reasoning
# Risks / Considerations
# Recommended Actions

Do not invent information."""

    try:
        answer = client.models.generate_content(
            model=GEMINI_MODEL, contents=prompt
        ).text.strip()
    except Exception as e:
        return {"answer": f"Decision error: {e}", "sources": []}

    sources = [
        {"document": c["source"], "page": c["page"]}
        for c in retrieved
    ]
    return {"answer": answer, "sources": sources}


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )
    
@app.post("/api/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    saved = []
    for file in files:
        extension = Path(file.filename).suffix.lower()
        if extension not in [".pdf", ".docx", ".txt"]:
            continue
        (UPLOAD_DIR / Path(file.filename).name).write_bytes(await file.read())
        saved.append(Path(file.filename).name)

    result = build_knowledge_base()
    result["files"] = saved
    return result


@app.post("/api/chat")
async def chat(data: dict):
    return generate_answer(data.get("question", ""))


@app.post("/api/summary")
async def summary(data: dict):
    return {"result": summarize_document(data.get("document", ""))}


@app.post("/api/compare")
async def compare(data: dict):
    return {
        "result": compare_documents(
            data.get("document_a", ""),
            data.get("document_b", "")
        )
    }


@app.post("/api/decision")
async def decision(data: dict):
    return decision_copilot(data.get("situation", ""))


@app.get("/api/documents")
async def get_documents():
    return {"documents": sorted({c["source"] for c in chunks})}


@app.get("/api/stats")
async def get_stats():
    return {
        "status": "Ready" if knowledge_base_ready else "Not Ready",
        "documents": len({c["source"] for c in chunks}),
        "sections": len(documents),
        "chunks": len(chunks),
        "vectors": faiss_index.ntotal if faiss_index else 0,
        "embedding_model": EMBEDDING_MODEL_NAME,
        "reranker": RERANKER_MODEL_NAME,
        "llm": GEMINI_MODEL
    }


@app.post("/api/clear-chat")
async def clear_chat():
    global conversation_history
    conversation_history = []
    return {"success": True}
