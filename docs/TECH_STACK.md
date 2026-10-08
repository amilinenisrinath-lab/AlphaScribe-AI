# Project Tech Stack & Justification

## System Overview
The **Multi-Agent Financial/Market Research Analyst** is a full-stack, enterprise-grade AI system. It automates financial document parsing (10-K, 10-Q, earnings calls), quantitative market ratio extraction, cross-document verification, and Wall Street-style investment memo synthesis.

---

## Complete Tech Stack Matrix

| Layer / Domain | Technology / Tool | Role & Purpose in Project | Resume Impact & Engineering Justification |
| :--- | :--- | :--- | :--- |
| **Frontend Framework** | **Next.js 14+ (React + TypeScript)** | Interactive investor portal, memo editor, and agent monitoring dashboard | Demonstrates modern enterprise UI and full-stack type safety |
| **Styling & Components** | **Tailwind CSS + shadcn/ui** | Clean, professional SaaS design system and layout | High-polish modern UI without bloated external dependencies |
| **Streaming UI** | **Server-Sent Events (SSE)** | Real-time streaming of agent reasoning steps, logs, and generated memo text | Mastery of asynchronous event-driven streaming architectures |
| **Data Visualization (Reports & PDF)** | **R (`ggplot2` / `tidyquant`)** | Script-driven generation of institutional-grade financial & econometric charts embedded in memos | **Polyglot Data Science flex:** Demonstrates Python-R interoperability and publication-grade data visualization |
| **Data Visualization (Web UI)** | **Recharts** | Interactive stock trend charts and interactive financial breakdown on the web | Clean, client-side dynamic data rendering |
| **Backend API** | **FastAPI (Python 3.11+)** | High-performance asynchronous REST & streaming API | The industry standard for production AI backend services |
| **Agent Orchestration** | **LangGraph** | Stateful multi-agent graph (Supervisor, Researcher, Analyst, Verifier, Writer) | Proves mastery of state machines, cyclical graphs, and agent collaboration |
| **Document Ingestion** | **PyMuPDF / pdfplumber + Vision LLM** | Ingesting and parsing earnings reports, financial tables, and PDF balance sheets | Demonstrates multimodal unstructured data extraction skills |
| **Vector Database** | **Qdrant (Local / Docker)** | Vector database with native **Hybrid Search** (Dense + BM25 Sparse) | Knowledge of production vector retrieval algorithms and hybrid indexing |
| **Embeddings & Reranker** | **BGE-M3 + BGE-Reranker** | Semantic search + cross-encoder reranking to ensure high context precision | Advanced RAG optimization preventing context dilution and hallucination |
| **Financial Tools** | **yfinance API & Python REPL** | Live ticker retrieval and deterministic programmatic financial calculations | Eliminates LLM math hallucination via deterministic code execution |
| **Database & ORM** | **SQLite + SQLModel / SQLAlchemy** | Lightweight, file-based relational database storing memos, sessions, and logs | Clean data modeling, portability, and zero-configuration local runs |
| **LLMOps & Tracing** | **LangSmith / Arize Phoenix** | Tracing multi-agent graph execution, latency, and token cost | Shows enterprise observability and telemetry awareness |
| **AI Evaluation (Evals)** | **Ragas** | Automated quantitative benchmark (Faithfulness, Relevance, Context Precision) | Evaluates AI reliability quantitatively using standard industry metrics |
| **DevOps & Containerization** | **Docker & Docker Compose** | Multi-container setup to run Frontend, Backend, and Qdrant with one command | Demonstrates containerization, portability, and DevOps fundamentals |

---

## Architectural Rationale

### 1. LangGraph over CrewAI
- **Cyclical State Graphs:** Real-world validation (like fact-checking financial claims) requires conditional looping back to earlier nodes. LangGraph natively models cyclical execution graphs with explicit state typing.
- **State Transparency:** All agents read and write to a typed state dictionary (`AgentState`), making state transitions deterministic and inspectable.

### 2. Hybrid Search (Dense + Sparse BM25) with Qdrant
- Pure vector embeddings fail on exact financial terminology (e.g., distinguishing between *"GAAP Operating Margin"* and *"Adjusted Non-GAAP Operating Margin"*).
- Hybrid search matches exact keywords via sparse indices and semantic intent via dense vectors, merged via Reciprocal Rank Fusion (RRF).

### 3. Dual-Engine Visualization (R + Recharts)
- **Web UI:** Recharts provides high frame-rate interactive visualizations in the browser.
- **Institutional Reports:** R's `ggplot2` is the gold standard for publication-grade financial charts. Triggering R scripts from Python illustrates cross-language data science capability.

### 4. SQLite + SQLModel
- Serverless, file-backed, and zero-setup. Anyone reviewing your code can clone the repo and immediately run tests without configuring Postgres credentials.
- SQLModel combines Pydantic validation with SQLAlchemy ORM, ensuring schema consistency across FastAPI endpoints and the DB layer.
