# System Architecture & Design

## 1. High-Level Architecture Flow

```mermaid
flowchart TD
    User([User / Browser]) <-->|Next.js 14 + Tailwind + SSE| UI[Frontend Dashboard]
    UI <-->|REST API + Server-Sent Events| Backend[FastAPI Backend]
    
    subgraph MultiAgentEngine [LangGraph Multi-Agent Orchestrator]
        Supervisor[Supervisor Agent]
        Researcher[Document & SEC Researcher]
        Analyst[Financial Math & Ratio Analyst]
        FactChecker[Fact-Checker & Citation Verifier]
        Writer[Investment Memo Writer]
        
        Supervisor -->|Delegate Retrieval| Researcher
        Supervisor -->|Delegate Metrics & R Plots| Analyst
        Supervisor -->|Synthesize Draft| Writer
        Writer -->|Verify Claims| FactChecker
        FactChecker -.->|Loop back if unverified| Researcher
        FactChecker -->|Verified| Complete([Final Memo])
    end
    
    Backend <--> MultiAgentEngine
    
    subgraph RetrievalLayer [Hybrid RAG Pipeline]
        DocParser[PDF & Table Parser: PyMuPDF]
        VectorDB[(Qdrant Vector DB: Dense + Sparse BM25)]
        Reranker[Cross-Encoder: BGE-Reranker]
        DocParser --> VectorDB --> Reranker
    end
    
    Researcher <--> RetrievalLayer
    Analyst <--> Tools[Tools: yfinance API + Python REPL + R ggplot2]
    
    subgraph Persistence [Storage & Telemetry]
        AppDB[(SQLite DB: SQLModel)]
        Tracing[LangSmith / Phoenix Telemetry]
    end
    
    Backend --> AppDB
    Backend --> Tracing
```

---

## 2. Multi-Agent Collaboration Protocol

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as Next.js Dashboard
    participant API as FastAPI (SSE Stream)
    participant Sup as Supervisor Node
    participant Res as Researcher Node
    participant Ana as Analyst Node
    participant Wri as Writer Node
    participant Ver as Fact-Checker Node
    
    User->>UI: Upload 10-K & Enter Ticker (e.g. AAPL)
    UI->>API: POST /api/analyze (Initiate Session)
    API-->>UI: SSE Stream Connected
    
    API->>Sup: Initialize AgentState
    Sup->>Res: Query 10-K disclosures (MD&A, Segment Revenue, Risks)
    Res-->>Sup: Return hybrid RAG chunks with source citations
    
    Sup->>Ana: Fetch live valuation & run financial ratios + R chart
    Ana-->>Sup: Return live multiples & generated ggplot2 chart paths
    
    Sup->>Wri: Compile draft investment memo
    Wri-->>Ver: Send draft memo with citation keys
    
    Ver->>Ver: Cross-reference every claim with retrieved 10-K context
    alt Hallucination / Unsupported Claim Detected
        Ver-->>Res: Loop back: Request additional verification context
    else All Claims Verified
        Ver-->>API: Emit Final Verified Memo
        API-->>UI: Stream Completed Markdown & Render Charts
    end
```

---

## 3. Agent Responsibilities & Tools

### A. Supervisor Agent
* **Role:** State machine coordinator and router.
* **Logic:** Evaluates current `AgentState`, determines missing information, and triggers specialized worker agents until all sections are fulfilled.

### B. Researcher Agent
* **Role:** Unstructured financial document extraction.
* **Tools:**
  * `hybrid_search_tool`: Queries Qdrant dense vector embeddings + sparse BM25 indices.
  * `rerank_filter`: Filters candidate text chunks using a cross-encoder model.

### C. Financial Analyst Agent
* **Role:** Quantitative market intelligence and deterministic calculation.
* **Tools:**
  * `yfinance_tool`: Live stock quotes, enterprise value, trailing P/E, revenue history.
  * `python_repl_tool`: Sandboxed code execution for deterministic financial metrics (e.g., CAGR, ROIC, debt service coverage).
  * `r_chart_tool`: Executes R scripts using `ggplot2` to generate institutional-grade PNG/SVG charts.

### D. Fact-Checker Agent
* **Role:** Zero-tolerance hallucination barrier.
* **Logic:**
  * Extracts all numerical assertions, quotes, and forward-looking statements in the draft memo.
  * Checks if each assertion is explicitly backed by an indexed chunk ID in the retrieved context.
  * If unverified, flags the state with feedback and forces a graph iteration.

### E. Writer Agent
* **Role:** Institutional synthesis and structuring.
* **Output Format:** Professional Markdown investment memo containing:
  * Executive Summary & Investment Thesis
  * Valuation Multiples Table
  * Operational & Segment Analysis
  * Embedded R `ggplot2` Visualizations
  * Key Risks & Footnote Citations

---

## 4. Database Schema (SQLite via SQLModel)

```mermaid
erDiagram
    SESSION ||--o{ DOCUMENT : has
    SESSION ||--o{ MEMO : generates
    SESSION ||--o{ AGENT_LOG : logs
    
    SESSION {
        string id PK
        string ticker
        datetime created_at
        string status
    }
    
    DOCUMENT {
        string id PK
        string session_id FK
        string file_name
        string file_path
        int total_pages
        int chunk_count
        datetime uploaded_at
    }
    
    MEMO {
        string id PK
        string session_id FK
        string title
        string markdown_content
        string status
        json chart_paths
        json citations
        datetime created_at
    }
    
    AGENT_LOG {
        string id PK
        string session_id FK
        string agent_name
        string action
        string details
        datetime timestamp
    }
```

---

## 5. Streaming API Contract

### `POST /api/analyze`
* **Request:**
  ```json
  {
    "ticker": "AAPL",
    "document_id": "doc_12345",
    "query": "Synthesize a 10-K investment memo focused on Services segment margins and CapEx."
  }
  ```
* **Response (SSE Event Stream):**
  * `event: node_start` $\to$ `{"node": "Researcher", "status": "Searching Qdrant for Services margin disclosures..."}`
  * `event: tool_call` $\to$ `{"tool": "r_chart_tool", "output": "/data/outputs/aapl_margins.png"}`
  * `event: verification` $\to$ `{"claims_verified": 14, "unverified": 0}`
  * `event: memo_chunk` $\to$ `{"delta": "### 1. Executive Summary\n\nApple's services revenue..."}`
  * `event: complete` $\to$ `{"memo_id": "memo_9876", "status": "COMPLETED"}`
