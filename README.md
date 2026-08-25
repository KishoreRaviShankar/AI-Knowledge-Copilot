AI Enterprise Knowledge Intelligence & Decision Copilot

An enterprise-focused Retrieval-Augmented Generation (RAG) application that lets users upload organizational documents and interact with their content through an AI-powered web interface.

The application combines semantic search, keyword search, reranking, and Gemini-based answer generation to produce grounded responses with source references.

<<<<<<< HEAD
Project Overview

Organizations store important knowledge across policies, manuals, reports, procedures, and guidelines. Finding the correct information manually can be slow and difficult. This project converts uploaded documents into a searchable knowledge base so users can ask questions, summarize content, compare documents, and receive decision support based only on the uploaded material.

Key Features

Upload multiple PDF, DOCX, and TXT files

Extract, clean, and split document text into overlapping chunks

Generate embeddings using Sentence Transformers

Perform semantic vector search with FAISS

Perform keyword retrieval with BM25

Combine results through hybrid retrieval

Rerank candidate chunks using a CrossEncoder

Generate grounded answers using the Gemini API

Show document names, page numbers, and relevance scores

Support conversational follow-up questions

Summarize individual documents

Compare two documents and identify differences

Provide document-grounded decision recommendations

Display knowledge-base statistics

Offer a responsive HTML, CSS, and JavaScript interface

How It Works

The user uploads supported documents.

Text is extracted and cleaned.

Text is divided into overlapping chunks.

Sentence Transformer embeddings are generated.

Embeddings are stored in a FAISS index.

A BM25 keyword index is also created.

A user query is searched against both indexes.

Candidate chunks are reranked using a CrossEncoder.

The highest-ranked chunks are supplied to Gemini as context.

Gemini returns an answer grounded in the retrieved content.

System Architecture


## Project Overview

Organizations store important knowledge across policies, manuals, reports, procedures, and guidelines. Finding the correct information manually can be slow and difficult. This project converts uploaded documents into a searchable knowledge base so users can ask questions, summarize content, compare documents, and receive decision support based only on the uploaded material.

## Key Features

- Upload multiple PDF, DOCX, and TXT files
- Extract, clean, and split document text into overlapping chunks
- Generate embeddings using Sentence Transformers
- Perform semantic vector search with FAISS
- Perform keyword retrieval with BM25
- Combine results through hybrid retrieval
- Rerank candidate chunks using a CrossEncoder
- Generate grounded answers using the Gemini API
- Show document names, page numbers, and relevance scores
- Support conversational follow-up questions
- Summarize individual documents
- Compare two documents and identify differences
- Provide document-grounded decision recommendations
- Display knowledge-base statistics
- Offer a responsive HTML, CSS, and JavaScript interface

## How It Works

1. The user uploads supported documents.
2. Text is extracted and cleaned.
3. Text is divided into overlapping chunks.
4. Sentence Transformer embeddings are generated.
5. Embeddings are stored in a FAISS index.
6. A BM25 keyword index is also created.
7. A user query is searched against both indexes.
8. Candidate chunks are reranked using a CrossEncoder.
9. The highest-ranked chunks are supplied to Gemini as context.
10. Gemini returns an answer grounded in the retrieved content.

## System Architecture


>>>>>>> 47aab9a (Expand project documentation)
flowchart TD
    A[Upload PDF, DOCX or TXT] --> B[Extract and clean text]
    B --> C[Create overlapping chunks]
    C --> D[Sentence Transformer embeddings]
    C --> E[BM25 keyword index]
    D --> F[FAISS vector index]
    G[User question] --> H[Hybrid retrieval]
    F --> H
    E --> H
    H --> I[CrossEncoder reranking]
    I --> J[Relevant context]
    J --> K[Gemini generation]
    K --> L[Answer with sources]
<<<<<<< HEAD

Technology Stack

Component

Technology

Backend

Python, FastAPI

Frontend

HTML, CSS, JavaScript, Jinja2

Document processing

pypdf, python-docx

Embedding model

all-MiniLM-L6-v2

Vector search

FAISS

Keyword retrieval

BM25

Reranker

cross-encoder/ms-marco-MiniLM-L-6-v2

Generative AI

Google Gemini API

Server

Uvicorn

Project Structure

=======


## Technology Stack

| Component | Technology |
| --- | --- |
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript, Jinja2 |
| Document processing | pypdf, python-docx |
| Embedding model | `all-MiniLM-L6-v2` |
| Vector search | FAISS |
| Keyword retrieval | BM25 |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| Generative AI | Google Gemini API |
| Server | Uvicorn |

## Project Structure

```text
>>>>>>> 47aab9a (Expand project documentation)
AI-Knowledge-Copilot/
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
├── data/
├── templates/
│   └── index.html
└── static/
    ├── style.css
    ├── script.js
    └── favicon.ico
<<<<<<< HEAD

The .env, virtual environment, cache files, and uploaded documents should not be committed to GitHub.

Installation and Setup

1. Clone the repository

git clone https://github.com/KishoreRaviShankar/AI-Knowledge-Copilot.git
cd AI-Knowledge-Copilot

2. Create a virtual environment

Windows PowerShell:

python -m venv .venv
.venv\Scripts\Activate.ps1

Windows Command Prompt:

=======
```

The `.env`, virtual environment, cache files, and uploaded documents should not be committed to GitHub.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/KishoreRaviShankar/AI-Knowledge-Copilot.git
cd AI-Knowledge-Copilot
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
>>>>>>> 47aab9a (Expand project documentation)
python -m venv .venv
.venv\Scripts\activate

macOS or Linux:

<<<<<<< HEAD
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
=======
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
>>>>>>> 47aab9a (Expand project documentation)

pip install -r requirements.txt

<<<<<<< HEAD
4. Configure Gemini

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key_here

Keep the key on one line. Do not add quotation marks or spaces around =. Never commit the real .env file.

5. Run the application
=======
### 4. Configure Gemini

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Keep the key on one line. Do not add quotation marks or spaces around `=`. Never commit the real `.env` file.

### 5. Run the application
>>>>>>> 47aab9a (Expand project documentation)

uvicorn app:app --reload

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

The first start can take longer because the embedding and reranking models may need to download.

API documentation:

<<<<<<< HEAD
http://127.0.0.1:8000/docs

The first start can take longer because the embedding and reranking models may need to download.

Usage

Open the application in a browser.

Upload PDF, DOCX, or TXT files.

Wait for the knowledge base to be built.

Open the Knowledge Assistant and ask a question.

Review the answer and its document sources.

Use Summarizer, Compare, or Decision Copilot when required.

API Endpoints

Method

Endpoint

Purpose

GET

/

Display the web interface

POST

/api/upload

Upload files and rebuild the knowledge base

POST

/api/chat

Ask questions about uploaded documents

POST

/api/summary

Summarize a selected document

POST

/api/compare

Compare two uploaded documents

POST

/api/decision

Generate document-grounded decision support

GET

/api/documents

List indexed documents

GET

/api/stats

Return knowledge-base statistics

Example Questions

What are the eligibility requirements described in the documents?

Summarize the important rules in the academic policy.

What is the placement procedure?

Compare the old and new organizational policies.

What action should be taken according to the uploaded documents?

Retrieval Configuration

The principal retrieval settings are defined near the beginning of app.py:

=======
1. Open the application in a browser.
2. Upload PDF, DOCX, or TXT files.
3. Wait for the knowledge base to be built.
4. Open the Knowledge Assistant and ask a question.
5. Review the answer and its document sources.
6. Use Summarizer, Compare, or Decision Copilot when required.

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Display the web interface |
| `POST` | `/api/upload` | Upload files and rebuild the knowledge base |
| `POST` | `/api/chat` | Ask questions about uploaded documents |
| `POST` | `/api/summary` | Summarize a selected document |
| `POST` | `/api/compare` | Compare two uploaded documents |
| `POST` | `/api/decision` | Generate document-grounded decision support |
| `GET` | `/api/documents` | List indexed documents |
| `GET` | `/api/stats` | Return knowledge-base statistics |

## Example Questions

- What are the eligibility requirements described in the documents?
- Summarize the important rules in the academic policy.
- What is the placement procedure?
- Compare the old and new organizational policies.
- What action should be taken according to the uploaded documents?

## Retrieval Configuration

The principal retrieval settings are defined near the beginning of `app.py`:

```python
>>>>>>> 47aab9a (Expand project documentation)
CHUNK_SIZE = 350
CHUNK_OVERLAP = 75
SEMANTIC_TOP_K = 12
KEYWORD_TOP_K = 12
FINAL_TOP_K = 5
SIMILARITY_THRESHOLD = 0.20
<<<<<<< HEAD

These values can be tuned based on document size, retrieval quality, response speed, and system resources.

Security and Privacy

API keys are loaded from .env instead of being hard-coded.

Answers are instructed to use only retrieved organizational context.

Unsupported file types are ignored.

Uploaded filenames are reduced to their base names before saving.

Documents are stored locally in the data directory.

Production deployments should add authentication, file-size limits, malware scanning, rate limiting, and user-specific storage.

Current Limitations

FAISS and BM25 indexes are stored in memory and rebuilt after uploads.

Conversation history is global rather than separated by user session.

Uploaded documents share one local directory.

Scanned PDFs require OCR, which is not currently included.

Very large documents are truncated for summary and comparison operations.

Gemini responses require an internet connection.

Future Improvements

Add OCR support for scanned PDFs

Save and reload vector indexes from disk

Add authentication and separate user workspaces

Store conversation history in a database

Stream generated answers to the interface

Add document deletion and knowledge-base management

Add safer file validation and upload controls

Evaluate retrieval using precision, recall, MRR, and faithfulness metrics

Add Docker and deployment configurations

Add automated tests and CI/CD

Troubleshooting

GEMINI_API_KEY is missing from .env

Confirm that .env is beside app.py and contains:

GEMINI_API_KEY=your_actual_key

Illegal header value

The API key contains a line break, quotation mark, space, or extra character. Keep the complete key on one line and restart the server.

Hugging Face unauthenticated warning

This is normally a warning, not an application error. Models can still download, although authenticated requests may receive higher limits.

/favicon.ico returns 404

Add favicon.ico to the static directory and reference it from the <head> of index.html, or ignore the request when no favicon is required.

Disclaimer

AI-generated answers should be reviewed before being used for important organizational, legal, financial, or policy decisions. Accuracy depends on the quality and completeness of the uploaded documents.

Author

Kishore Ravi Shankar

GitHub: KishoreRaviShankar

License

This project is intended for educational and portfolio use. Add a LICENSE file to define permissions for reuse, modification, and distribution.
=======
```

These values can be tuned based on document size, retrieval quality, response speed, and system resources.

## Security and Privacy

- API keys are loaded from `.env` instead of being hard-coded.
- Answers are instructed to use only retrieved organizational context.
- Unsupported file types are ignored.
- Uploaded filenames are reduced to their base names before saving.
- Documents are stored locally in the `data` directory.
- Production deployments should add authentication, file-size limits, malware scanning, rate limiting, and user-specific storage.

## Current Limitations

- FAISS and BM25 indexes are stored in memory and rebuilt after uploads.
- Conversation history is global rather than separated by user session.
- Uploaded documents share one local directory.
- Scanned PDFs require OCR, which is not currently included.
- Very large documents are truncated for summary and comparison operations.
- Gemini responses require an internet connection.

## Future Improvements

- Add OCR support for scanned PDFs
- Save and reload vector indexes from disk
- Add authentication and separate user workspaces
- Store conversation history in a database
- Stream generated answers to the interface
- Add document deletion and knowledge-base management
- Add safer file validation and upload controls
- Evaluate retrieval using precision, recall, MRR, and faithfulness metrics
- Add Docker and deployment configurations
- Add automated tests and CI/CD

## Troubleshooting

### `GEMINI_API_KEY is missing from .env`

Confirm that `.env` is beside `app.py` and contains:

```env
GEMINI_API_KEY=your_actual_key
```

### `Illegal header value`

The API key contains a line break, quotation mark, space, or extra character. Keep the complete key on one line and restart the server.

### Hugging Face unauthenticated warning

This is normally a warning, not an application error. Models can still download, although authenticated requests may receive higher limits.

### `/favicon.ico` returns 404

Add `favicon.ico` to the `static` directory and reference it from the `<head>` of `index.html`, or ignore the request when no favicon is required.

## Disclaimer

AI-generated answers should be reviewed before being used for important organizational, legal, financial, or policy decisions. Accuracy depends on the quality and completeness of the uploaded documents.

## Author

**Kishore Ravi Shankar**

GitHub: [KishoreRaviShankar](https://github.com/KishoreRaviShankar)

## License

This project is intended for educational and portfolio use. Add a `LICENSE` file to define permissions for reuse, modification, and distribution.
>>>>>>> 47aab9a (Expand project documentation)
