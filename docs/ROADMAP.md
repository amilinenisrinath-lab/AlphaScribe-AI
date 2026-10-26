# AlphaScribe AI: Project Execution Roadmap (Phases 1 to 6)

This document defines the step-by-step development roadmap for **AlphaScribe AI**.

---

## Phase 1: Project Scaffolding & Database Setup (COMPLETED)
* **Goal:** Initialize directories, environment configurations, and the local SQLite database.
* **Key Tasks:**
  - [x] Create standardized project directory structure (`docs/`, `backend/`, `frontend/`).
  - [x] Configure `.gitignore` for Python, SQLite, Next.js, and R.
  - [x] Write Python dependencies in `backend/requirements.txt`.
  - [x] Configure `backend/app/core/config.py` with environment variable loading.
  - [x] Create `backend/app/db/session.py` and `models.py` using **SQLModel** (Sessions, Documents, Memos, Agent Logs).
  - [x] Scaffold Next.js 14 frontend skeleton (`frontend/package.json`, `tsconfig.json`, `tailwind.config.js`).
  - [x] Verify SQLite database schema, timezone-aware fields, and CRUD operations via `test_phase1_db.py`.
  - [x] Verify FastAPI lifespan startup and health checks via `test_api_health.py`.
* **Acceptance Criteria:** SQLite database creates tables automatically on FastAPI startup; API endpoints return 200 OK. [PASSED]

---

## Phase 2: Multimodal Ingestion & Advanced Hybrid RAG Engine (COMPLETED)
* **Goal:** Ingest complex 10-K/10-Q PDFs and build high-precision hybrid retrieval.
* **Key Tasks:**
  - [x] Implement `backend/app/rag/parser.py` using `PyMuPDF` to extract structured sections and tables.
  - [x] Build table-aware chunking preserving financial balance sheets and disclosures.
  - [x] Configure Qdrant vector store (`backend/app/rag/vector_store.py`) with native **Hybrid Search** (Dense Cosine + Sparse BM25 Reciprocal Rank Fusion) and singleton client architecture.
  - [x] Implement cross-encoder reranker (`backend/app/rag/reranker.py`) for high-precision passage pruning.
  - [x] Expose file upload API endpoint (`POST /api/documents/upload`) with automated SQLite metadata logging.
  - [x] Pass automated Phase 2 test suite (`backend/tests/test_phase2_rag.py`) with authentic 10-K test filings.
* **Acceptance Criteria:** Uploaded 10-K PDF is parsed, indexed in Qdrant, and retrieved with accurate financial table citations. [PASSED - 100%]

---

## Phase 3: Financial Analysis Tools & R Visualization Engine (COMPLETED)
* **Goal:** Implement deterministic math calculations and the Python-to-R visualization pipeline.
* **Key Tasks:**
  - [x] Build `backend/app/tools/yfinance_tool.py` for live market data (quotes, historical earnings, valuation ratios) with resilient fallback data.
  - [x] Build `backend/app/tools/python_repl_tool.py` for deterministic calculation of financial ratios (CAGR, margins, debt-to-equity) eliminating LLM math hallucinations.
  - [x] Implement `backend/r_scripts/financial_plots.R` utilizing `ggplot2` for publication-grade financial charts.
  - [x] Implement `backend/app/tools/r_chart_tool.py` bridging Rscript execution with high-resolution 300 DPI Python plotting fallback.
  - [x] Pass automated Phase 3 test suite (`backend/tests/test_phase3_tools.py`) verifying arithmetic accuracy and chart asset generation.
* **Acceptance Criteria:** Python calls R script / high-res engine, passes ticker & metrics JSON, and receives an institutional-quality chart image. [PASSED - 100%]

---

## Phase 4: LangGraph Multi-Agent Orchestration (COMPLETED)
* **Goal:** Assemble the multi-agent state machine with cyclical verification.
* **Key Tasks:**
  - [x] Define state dictionary schema in `backend/app/agents/state.py` (`AgentState`).
  - [x] Implement specialized agent node functions:
    - `supervisor.py` (State-machine coordinator & dynamic routing logic).
    - `researcher.py` (Hybrid RAG extraction of SEC 10-K disclosures & segment margins).
    - `analyst.py` (Pulls live multiples, executes deterministic Python math, renders R charts).
    - `writer.py` (Synthesizes institutional Markdown memos with citation links).
    - `fact_checker.py` (Zero-hallucination verification audit against source chunks & arithmetic).
  - [x] Compile cyclical state graph in `backend/app/agents/graph.py` with dynamic review loop for rejected assertions.
  - [x] Pass automated Phase 4 test suite (`backend/tests/test_phase4_agents.py`) verifying individual nodes, cyclical guardrails, and full workflow execution.
* **Acceptance Criteria:** Given a ticker and question, agents collaborate autonomously to output a verified markdown investment memo. [PASSED - 100%]

---

## Phase 5: FastAPI Streaming API & Next.js UI (COMPLETED)
* **Goal:** Connect backend and frontend via Server-Sent Events (SSE) and provide a polished UI.
* **Key Tasks:**
  - [x] Build FastAPI SSE streaming endpoint (`GET /api/analyze/stream`).
  - [x] Develop Next.js dashboard UI:
    - File upload dropzone for financial reports.
    - Real-time agent status tracker (shows node steps, reasoning, and tool calls).
    - Interactive Memo viewer with markdown rendering, citation tooltips, and embedded R charts.
    - Client-side interactive stock charts using **Recharts**.
    - Export button for downloading PDF / Markdown reports.
* **Acceptance Criteria:** Full end-to-end user flow working smoothly in the browser with real-time streaming verified via automated integration tests and Next.js production build.

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
