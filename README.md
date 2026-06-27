# RAG MCQ Generator

An AI-powered system that generates high-quality multiple-choice questions (MCQs) from educational content using Retrieval-Augmented Generation (RAG). Designed for HSSC Pre-Engineering students (Classes 11–12) covering Mathematics, Physics, and English.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [API Reference](#api-reference)
- [Data Schemas](#data-schemas)
- [Configuration](#configuration)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [Features](#features)

---

## Overview

The system combines a **hybrid retrieval pipeline** (dense semantic search + keyword matching) with **Google Gemini 2.5-Flash** to produce contextually accurate MCQs grounded in curriculum content. Source material is stored as Markdown files, chunked with full hierarchy metadata, embedded using BAAI/BGE-M3, and indexed in FAISS for fast retrieval.

**Supported Subjects**: Mathematics (Class 11 & 12), Physics (Class 11 & 12), English *(Physics/English endpoints planned)*

---

## Architecture

```
┌─────────────────────────────────────┐
│        Frontend (Next.js)            │
│  Subject → Topic → Difficulty → Qty  │
└──────────────┬──────────────────────┘
               │  POST /mcq_math
               ▼
┌─────────────────────────────────────┐
│         FastAPI Backend              │
│                                      │
│  1. Hybrid Retrieval                 │
│     ├─ Dense: FAISS + BGE-M3        │
│     └─ Keyword: Section ID matching │
│                                      │
│  2. MCQ Generation                   │
│     └─ Gemini 2.5-Flash API         │
│                                      │
│  3. Validation                       │
│     ├─ Pydantic schema check        │
│     ├─ Semantic uniqueness          │
│     └─ Distractor critique          │
│                                      │
│  4. Return structured MCQ JSON       │
└─────────────────────────────────────┘
               │
     ┌─────────┴──────────┐
     │  Prebuilt Assets    │
     │  ├─ FAISS index     │
     │  ├─ Chunk embeddings│
     │  └─ Markdown source │
     └────────────────────┘
```

### Request Flow

1. User selects subject, enters a topic/chapter, chooses difficulty and quantity
2. Frontend sends `POST /mcq_math` with the query, difficulty, and count
3. Backend encodes the query with BGE-M3 and searches the FAISS index (top-k=10, similarity threshold=0.8)
4. Numeric patterns in the query (e.g. "3.1") additionally match section IDs directly
5. Retrieved chunks are formatted as context and passed to Gemini with a structured prompt
6. Gemini returns JSON MCQs which are parsed, validated with Pydantic, and returned
7. Frontend renders MCQs with answer selection, scoring, and explanations

---

## Project Structure

```
rag_mcq_generator/
├── .env                          # Google API key (project root, not tracked)
├── requirements.txt              # Backend Python dependencies
│
├── frontend/                     # Next.js 16 + React 19 + TypeScript
│   ├── app/
│   │   ├── layout.tsx            # Root layout
│   │   ├── page.tsx              # Subject selection home page
│   │   └── mcq/[subject]/
│   │       ├── page.tsx          # MCQ page router
│   │       └── mcq-page-client.tsx  # Main MCQ UI (form + results)
│   ├── components/
│   │   ├── mcq-form.tsx          # Input form (topic, difficulty, quantity)
│   │   ├── mcq-results.tsx       # Results display with scoring
│   │   ├── mcq-accordion.tsx     # Individual MCQ accordion component
│   │   ├── progress-indicator.tsx
│   │   ├── breadcrumb-nav.tsx
│   │   └── ui/                   # 40+ Radix UI component wrappers
│   ├── lib/
│   │   ├── types.ts              # MCQ, MCQOption TypeScript interfaces
│   │   ├── placeholders.ts       # Demo MCQs for initial display
│   │   └── utils.ts
│   ├── hooks/
│   │   ├── use-toast.ts
│   │   └── use-mobile.ts
│   ├── next.config.mjs
│   ├── tailwind.config.ts
│   └── package.json
│
└── mcqs_rag/                     # FastAPI Backend
    ├── main.py                   # API app: /ping, /mcq_math endpoints
    ├── pipeline.py               # Standalone CLI pipeline (for testing)
    ├── utility.py                # Load chunks & FAISS index utilities
    ├── reproductibilty.py        # Global config constants
    ├── requirements.txt          # Backend-specific dependencies
    │
    ├── mcq_schema/
    │   └── schema.py             # Pydantic MCQ model
    │
    ├── model/
    │   ├── generate_mcqs.py      # Main MCQ generation (Gemini API, retry logic)
    │   ├── prompt.py             # Prompt engineering for Gemini
    │   ├── embedding_model.py    # BGE-M3 loader
    │   ├── model_cache.py        # Global model cache (avoids reloading)
    │   ├── generate_embeddings.py  # Offline embedding generation pipeline
    │   └── semantic_uniqueness_model.py  # Sentence-BERT for deduplication
    │
    ├── chunking/
    │   ├── create_chunks.py      # Markdown chunker with hierarchy metadata
    │   ├── constants.py          # Chapter definitions (MATH_11_CHAPTERS, etc.)
    │   └── blueprint.py          # Hierarchical structure visualization
    │
    ├── retrieval/
    │   ├── hybrid_retrieval.py   # Dense + keyword retrieval, deduplication
    │   └── indexing.py           # FAISS index builder
    │
    ├── data_loading/
    │   └── data_ingestion.py     # File path constants and readers
    │
    ├── validation_suites/
    │   ├── uniqueness.py         # Semantic similarity deduplication
    │   ├── distractors.py        # Distractor quality critique via Gemini
    │   ├── citation_checker.py   # Source citation validation
    │   └── latex_checker.py      # LaTeX notation validation
    │
    ├── adaptive_module/          # Experimental adaptive learning
    │   ├── difficulty_schema.py
    │   ├── initalize_stats.py
    │   ├── select_next_topic.py
    │   └── update_topic_stats.py
    │
    ├── markdown/                 # Source curriculum content
    │   ├── MATH 11.md
    │   ├── MATH 12.md
    │   ├── PHY 11.md
    │   └── PHY 12.md
    │
    └── index/                    # Pre-built FAISS index (generated offline)
        └── syllabus.index
```

---

## Tech Stack

### Backend

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI 0.104+ (async) |
| Server | Uvicorn (ASGI) |
| LLM | Google Gemini 2.5-Flash |
| Embeddings | BAAI/BGE-M3 (via SentenceTransformers) |
| Vector Search | FAISS |
| Uniqueness Check | Sentence-BERT (all-MiniLM-L6-v2) |
| Validation | Pydantic v2 |
| ML Framework | PyTorch 2.6.0 |

### Frontend

| Component | Technology |
|-----------|-----------|
| Framework | Next.js 16.0.10 |
| UI Library | React 19.2.0 + TypeScript 5 |
| Components | Radix UI (40+ accessible primitives) |
| Styling | Tailwind CSS 4.1.9 |
| Math Rendering | KaTeX 0.16.27 |
| Forms | React Hook Form + Zod |
| Notifications | Sonner |
| Icons | Lucide React |

---

## API Reference

### `GET /ping`

Health check endpoint.

**Response**
```json
{ "message": "pong" }
```

---

### `POST /mcq_math`

Generate MCQs for a Mathematics topic.

**Request Body**
```json
{
  "query": "Generate questions on quadratic equations from section 3.1",
  "difficulty": "medium",
  "num_questions": 5
}
```

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `query` | string | Yes | — | min length 3 |
| `difficulty` | `"easy"` \| `"medium"` \| `"hard"` | No | `"medium"` | — |
| `num_questions` | integer | No | `5` | 1–20 |

**Response (200)**
```json
{
  "subject": "maths",
  "mcqs": [
    {
      "question": "What are the roots of x² - 5x + 6 = 0?",
      "A": "x = 1, x = 6",
      "B": "x = 2, x = 3",
      "C": "x = -2, x = -3",
      "D": "x = 3, x = 4",
      "correct": "B",
      "citation": "(Chapter 3, Section 1)",
      "explanation": "Using the quadratic formula or factoring: (x-2)(x-3)=0, so x=2 or x=3.",
      "isLatex": false
    }
  ]
}
```

**Response (500)**
```json
{ "detail": "Error message describing the failure" }
```

> **Note**: Physics (`/mcq_physic`) and English (`/mcq_english`) endpoints are referenced in the frontend but not yet implemented in the backend.

---

## Data Schemas

### Backend — `MCQ` (Pydantic, `mcq_schema/schema.py`)

```python
class MCQ(BaseModel):
    question: str       # The question text (may contain LaTeX)
    A: str              # Option A
    B: str              # Option B
    C: str              # Option C
    D: str              # Option D
    correct: str        # Correct option key: "A", "B", "C", or "D"
    citation: str       # Source reference, e.g. "(Chapter 3, Section 1)"
    explanation: str    # Step-by-step solution explanation
    isLatex: bool       # Whether question/options contain LaTeX notation
```

### Frontend — `MCQ` Interface (`lib/types.ts`)

```typescript
interface MCQ {
  question: string
  options: MCQOption               // { A, B, C, D }
  answer: "A" | "B" | "C" | "D"  // Correct answer key
  explanation?: string
  citation?: string
  isLatex?: boolean
}

interface MCQOption {
  A: string
  B: string
  C: string
  D: string
}
```

### Chunk Structure (internal, stored in JSON + FAISS index)

```python
{
  "chunk_index": int,
  "type": str,           # "chapter", "header", "exercise", "full_document"
  "section": str,        # Numeric ID e.g. "3.1"
  "chapter_id": str,
  "section_id": str,
  "subsection_id": str,
  "chapter_name": str,
  "section_name": str,
  "subsection_name": str,
  "title": str,
  "content": str,        # Text content that was embedded
  "embedding": list,     # BGE-M3 float vector
  "header_level": int,
  "char_count": int,
  "word_count": int,
  "source": str          # Source markdown file path
}
```

---

## Configuration

### Backend Constants (`mcqs_rag/reproductibilty.py`)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `top_k` | `10` | Top chunks to retrieve from FAISS |
| `min_similarity` | `0.8` | Minimum cosine similarity for dense retrieval |
| `seed` | `42` | Random seed |
| `embedding_model` | `"BAAI/bge-m3"` | Embedding model for chunks and queries |
| `semantic_similarity_model` | `"all-MiniLM-L6-v2"` | Model for uniqueness checking |
| `mcq_generation_model` | `"gemini-2.5-flash"` | Gemini model for MCQ generation |
| `semantic_similarity_threshold` | `0.85` | Threshold for duplicate MCQ detection |

### Environment Variables

| Variable | Location | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | `.env` (project root) | Required — Google API key with Gemini enabled |
| `NEXT_PUBLIC_API_BASE_URL` | `frontend/.env.local` | Backend URL for the frontend to call |

---

## Setup & Installation

### Prerequisites

- Python 3.9+
- Node.js 18+ (with npm or pnpm)
- Google API Key with Gemini API enabled

### Backend

```bash
# 1. Enter the backend directory
cd mcqs_rag

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r ../requirements.txt

# 4. Set up environment variables (in the PROJECT ROOT, not mcqs_rag/)
cd ..
echo "GOOGLE_API_KEY=your_key_here" > .env
```

### Frontend

```bash
# 1. Enter the frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Create environment file
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local
```

### Data Preparation (One-time, offline)

If the FAISS index and chunk embeddings are not pre-built, generate them:

```bash
cd mcqs_rag

# Chunk the markdown source files
python chunking/create_chunks.py

# Generate BGE-M3 embeddings for all chunks
python model/generate_embeddings.py

# Build the FAISS index
python retrieval/indexing.py
```

---

## Running the Application

### Backend (FastAPI)

```bash
cd mcqs_rag
source venv/bin/activate
uvicorn main:app --reload
# API available at: http://localhost:8000
# Interactive docs: http://localhost:8000/docs
```

### Frontend (Next.js)

```bash
cd frontend
npm run dev
# UI available at: http://localhost:3000
```

### CLI Pipeline (for testing without the API)

```bash
cd mcqs_rag
python pipeline.py \
  --file_path "markdown/MATH 11.md" \
  --query "quadratic functions from section 3.1"
```

---

## Features

### Backend

- **Hybrid Retrieval**: Combines dense semantic search (BGE-M3 + FAISS) with numeric section ID matching (e.g. "3.1") for high-precision chunk selection
- **Gemini MCQ Generation**: Structured prompt engineering with difficulty guidelines, retry logic (up to 3 attempts), and safe JSON parsing
- **Validation Pipeline**: Pydantic schema enforcement, semantic uniqueness checking (cosine similarity > 0.85 filtered), distractor quality critique via Gemini, and LaTeX validation
- **Model Caching**: Embedding models and Gemini client are cached globally at startup to avoid per-request reload overhead
- **Adaptive Learning Module** *(experimental)*: Tracks learner performance per topic and dynamically selects next questions by difficulty

### Frontend

- **Multi-subject navigation** with subject-specific demo MCQs
- **Interactive MCQ form**: free-text topic input, difficulty selector, question count (5/10/15)
- **Rich answer interface**: selectable options with visual feedback, post-submit answer reveal, step-by-step explanations, citations
- **KaTeX rendering** for mathematical LaTeX expressions
- **Export**: copy results as JSON or plaintext
- **Demo mode**: pre-loaded placeholder MCQs for UI testing without backend
- **Responsive dark-themed UI** built with Radix UI + Tailwind CSS
