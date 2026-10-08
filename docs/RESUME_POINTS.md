# Resume Bullets & Interview Talking Points: AlphaScribe AI

## 1. Resume Project Bullets (Copy & Paste Ready)

Add this under the **Projects** section of your resume:

### **AlphaScribe AI: Multi-Agent Financial Research Analyst (LangGraph, Next.js, R, Qdrant)**
* **Architected an autonomous multi-agent research platform** using **LangGraph** orchestrating 5 specialized nodes (Supervisor, Researcher, Analyst, Writer, Fact-Checker) to synthesize verifiable institutional investment memos from SEC 10-K filings.
* **Engineered an Advanced Hybrid RAG pipeline** combining dense cosine embeddings with sparse **BM25 keyword search** and **cross-encoder reranking** in **Qdrant**, achieving high-precision retrieval over complex multi-column financial tables and balance sheets.
* **Eliminated LLM arithmetic hallucinations** by integrating a sandboxed **Python REPL** tool for deterministic ratio calculations (CAGR, ROIC, debt service) and real-time market data via **yfinance**.
* **Developed a polyglot visualization bridge** executing **R (`ggplot2`)** scripts via subprocesses to generate publication-grade financial charts alongside interactive client-side **Recharts** visualizations.
* **Constructed an event-driven full-stack system** using **FastAPI** with **Server-Sent Events (SSE)** for real-time agent thought streaming, **SQLite (SQLModel)** for state persistence, and a modern **Next.js 14 (TypeScript, Tailwind CSS)** investor portal.
* **Benchmarked system reliability quantitatively** using the **Ragas** framework, achieving **>95% Faithfulness and Answer Relevance** across benchmark SEC 10-K test cases.

---

## 2. Interview Q&A Preparation

### Q1: What inspired you to build AlphaScribe AI?
> **Answer:**  
> *"Financial analysts spend dozens of hours reviewing SEC 10-K filings, transcribing tables into spreadsheets, and verifying disclosures. While LLMs are great at text, standard chatbots fail in finance because they hallucinate numbers, fail on exact table lookups, and cannot produce audited citations. I built **AlphaScribe AI** as a production-grade multi-agent platform with deterministic tools, hybrid retrieval, and automated fact-checking to solve these exact industry pain points."*

---

### Q2: Why did you choose LangGraph over simpler frameworks like CrewAI or basic LangChain chains?
> **Answer:**  
> *"Financial research cannot rely on linear chains because facts need verification loops. LangGraph allows explicit cyclical graph design and typed state management (`AgentState`). If my Fact-Checker node detects an assertion that lacks an explicit citation chunk ID from the ingested 10-K, the graph conditionally loops back to the Researcher node rather than hallucinating. This deterministic control is essential for enterprise AI."*

---

### Q3: How did you handle retrieval over complex financial tables where standard vector search often fails?
> **Answer:**  
> *"Standard vector embeddings struggle with exact financial phrases like 'Adjusted EBITDA' vs. 'GAAP Net Income' and dilute table rows. I solved this by implementing **Hybrid Search**: combining dense semantic vectors with sparse BM25 keyword matching via Reciprocal Rank Fusion (RRF) in Qdrant. Furthermore, my parser preserves Markdown table layouts as discrete high-priority chunks and passes candidate chunks through a cross-encoder reranker to prune noise."*

---

### Q4: Why combine Python and R in the same project?
> **Answer:**  
> *"In data science and quantitative finance, Python is the gold standard for microservices, API servers, and agent orchestration, while R and `ggplot2` remain unbeatable for publication-grade econometric graphics. Rather than compromising on aesthetic quality, I designed a Python tool that safely pipes extracted time-series data to an R script, compiling high-res PNG plots embedded directly into the final Markdown memo, with client-side interactive Recharts for the web dashboard."*

---

### Q5: How do you measure whether your agents are actually performing well?
> **Answer:**  
> *"I implemented automated quantitative evaluations using the **Ragas** framework (`eval_ragas.py`). Instead of guessing based on gut feeling, we measure three key metrics on a benchmark dataset: **Faithfulness** (ensuring claims are strictly grounded in retrieved SEC text), **Answer Relevance** (alignment with user queries), and **Context Precision** (evaluating how effectively our hybrid retrieval filtered noise)."*
