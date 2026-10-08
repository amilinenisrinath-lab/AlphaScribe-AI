# Project Execution Roadmap: Phases 1 to 6

This document defines the step-by-step development roadmap for the **Multi-Agent Financial/Market Research Analyst** system.

---

## Phase 1: Project Scaffolding & Database Setup
* **Goal:** Initialize directories, environment configurations, and the local SQLite database.
* **Key Tasks:**
  - [x] Create standardized project directory structure (`docs/`, `backend/`, `frontend/`).
  - [x] Configure `.gitignore` for Python, SQLite, Next.js, and R.
  - [ ] Write Python dependencies in `backend/requirements.txt`.
  - [ ] Configure `backend/app/core/config.py` with environment variable loading.
  - [ ] Create `backend/app/db/session.py` and `models.py` using **SQLModel** (Sessions, Documents, Memos, Agent Logs).
  - [ ] Scaffold Next.js 14 frontend skeleton (`frontend/package.json`, `tsconfig.json`, `tailwind.config.js`).
* **Acceptance Criteria:** SQLite database creates tables automatically on FastAPI startup; frontend displays base layout.

---

## Phase 2: Multimodal Ingestion & Advanced Hybrid RAG Engine
* **Goal:** Ingest complex 10-K/10-Q PDFs and build high-precision hybrid retrieval.
* **Key Tasks:**
  - [ ] Implement `backend/app/rag/parser.py` using `PyMuPDF` / `pdfplumber` to extract structured sections and tables.
  - [ ] Build table-aware chunking preserving financial balance sheets.
  - [ ] Configure Qdrant vector store (`backend/app/rag/vector_store.py`) with hybrid index (Dense embeddings + Sparse BM25).
  - [ ] Implement cross-encoder reranker (`backend/app/rag/reranker.py`) using FlashRank or BGE-Reranker.
  - [ ] Expose file upload API endpoint (`POST /api/documents/upload`).
* **Acceptance Criteria:** Uploaded 10-K PDF is parsed, indexed in Qdrant, and retrieved with accurate financial table citations.

---

## Phase 3: Financial Analysis Tools & R Visualization Engine
* **Goal:** Implement deterministic math calculations and the Python-to-R visualization pipeline.
* **Key Tasks:**
  - [ ] Build `backend/app/tools/yfinance_tool.py` for live market data (quotes, historical earnings, valuation ratios).
  - [ ] Build `backend/app/tools/python_repl_tool.py` for deterministic calculation of financial ratios (CAGR, EBITDA margins, debt service ratios).
  - [ ] Implement `backend/r_scripts/financial_plots.R` utilizing `ggplot2` and `tidyquant` for publication-quality charts.
  - [ ] Implement `backend/app/tools/r_chart_tool.py` to trigger R scripts from Python via `subprocess` and save PNG/SVG assets to `/data/outputs/`.
* **Acceptance Criteria:** Python calls R script, passes ticker & metrics JSON, and receives an institutional-quality chart image.

---

## Phase 4: LangGraph Multi-Agent Orchestration
* **Goal:** Assemble the multi-agent state machine with cyclical verification.
* **Key Tasks:**
  - [ ] Define state dictionary schema in `backend/app/agents/state.py` (`AgentState`).
  - [ ] Implement node functions:
    - `supervisor.py` (Orchestrates workflow, routes between nodes).
    - `researcher.py` (Executes Hybrid RAG queries for 10-K disclosures).
    - `analyst.py` (Runs financial tools, computes ratios, calls R plotting).
    - `fact_checker.py` (Validates every numeric statement against retrieved chunks).
    - `writer.py` (Drafts the structured Markdown investment memo).
  - [ ] Compile LangGraph state graph in `backend/app/agents/graph.py` with cyclical loop-back for unverified assertions.
* **Acceptance Criteria:** Given a ticker and question, agents collaborate autonomously to output a verified markdown investment memo.

---

## Phase 5: FastAPI Streaming API & Next.js UI
* **Goal:** Connect backend and frontend via Server-Sent Events (SSE) and provide a polished UI.
* **Key Tasks:**
  - [ ] Build FastAPI SSE streaming endpoint (`GET /api/analyze/stream`).
  - [ ] Develop Next.js dashboard UI:
    - File upload dropzone for financial reports.
    - Real-time agent status tracker (shows node steps, reasoning, and tool calls).
    - Interactive Memo viewer with markdown rendering, citation tooltips, and embedded R charts.
    - Client-side interactive stock charts using **Recharts**.
    - Export button for downloading PDF / Markdown reports.
* **Acceptance Criteria:** Full end-to-end user flow working smoothly in the browser with real-time streaming.

---

## Phase 6: Evals, Observability & Production Readiness (Resume Polish)
* **Goal:** Measure agent reliability quantitatively and package the repository for recruiters.
* **Key Tasks:**
  - [ ] Integrate **LangSmith** or **Arize Phoenix** for tracing token latency, agent graphs, and cost.
  - [ ] Implement automated evaluation script using **Ragas** (`backend/tests/eval_ragas.py`) measuring:
    - *Faithfulness*
    - *Answer Relevance*
    - *Context Precision*
  - [ ] Write `docker-compose.yml` to orchestrate Backend, Frontend, and Qdrant.
  - [ ] Write portfolio `README.md` with architecture diagrams, demo screenshots, and resume bullet points.
* **Acceptance Criteria:** One-command `docker compose up` starts the entire system; evals report quantitative benchmark scores.
