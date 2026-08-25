# AI Enterprise Knowledge Intelligence & Decision Copilot

FastAPI + HTML/CSS/JavaScript frontend for the RAG application.

## Features

- PDF, DOCX and TXT upload
- Document extraction
- Chunking
- SentenceTransformer embeddings
- FAISS vector search
- BM25 keyword search
- Hybrid retrieval
- CrossEncoder reranking
- Gemini answer generation
- Conversational follow-up questions
- Source references
- Document summarization
- Document comparison
- Decision Copilot
- Knowledge-base statistics
- Responsive web UI

## Setup

### 1. Create virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env` and add your Gemini API key:

```text
GEMINI_API_KEY=your_key_here
```

### 4. Run

```bash
uvicorn app:app --reload
```

Open:

http://127.0.0.1:8000

## Usage

1. Open Documents.
2. Upload PDF/DOCX/TXT files.
3. Click Build Knowledge Base.
4. Open Knowledge Assistant.
5. Ask questions.
6. Use Summarizer, Compare, or Decision Copilot as required.

Uploaded documents are stored in `data/`.
