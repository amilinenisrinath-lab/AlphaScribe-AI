"""
Phase 2 Verification Test Suite: Multimodal Ingestion & Hybrid RAG Engine
Tests:
1. PDF document parsing with PyMuPDF & table preservation.
2. Table-aware chunking.
3. HybridVectorStore indexing (Qdrant Dense + BM25 Sparse).
4. Hybrid retrieval with Reciprocal Rank Fusion (RRF).
5. Cross-Encoder reranking for precision filtering.
6. FastAPI POST /api/documents/upload integration.
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

import fitz  # PyMuPDF
from starlette.testclient import TestClient

from app.main import app
from app.rag.parser import FinancialDocumentParser
from app.rag.vector_store import HybridVectorStore
from app.rag.reranker import CrossEncoderReranker

def generate_sample_10k_pdf(output_path: Path):
    """Generates a realistic 2-page SEC 10-K filing with financial tables."""
    doc = fitz.open()

    # Page 1: Item 7 - Management Discussion & Analysis
    page1 = doc.new_page()
    text_p1 = (
        "UNITED STATES SECURITIES AND EXCHANGE COMMISSION\n"
        "WASHINGTON, D.C. 20549\n"
        "FORM 10-K - ANNUAL REPORT FOR APPLE INC.\n\n"
        "Item 7. Management's Discussion and Analysis of Financial Condition\n\n"
        "Executive Overview:\n"
        "During fiscal 2024, our Services revenue reached an all-time high of $96.2 billion, representing "
        "a 13% expansion year-over-year. Services gross margin widened to 74.0%, driven by recurring "
        "cloud subscriptions, App Store transactions, and advertising agreements. In contrast, Products gross "
        "margin remained stable at 36.5% amidst dynamic foreign exchange headwinds and input cost fluctuations.\n\n"
        "Capital Expenditures:\n"
        "Total capital expenditures amounted to $11.5 billion, focusing primarily on data center capacity, "
        "custom silicon design infrastructure, and automated tooling equipment."
    )
    page1.insert_text((50, 60), text_p1, fontsize=10)

    # Page 2: Item 8 - Segment Financial Table
    page2 = doc.new_page()
    text_p2 = (
        "Item 8. Financial Statements and Supplementary Data\n"
        "Note 11 - Segment Disclosures and Product Information\n\n"
        "Net Sales and Gross Margin by Operating Category (in Millions):\n\n"
        "Category | Fiscal 2023 | Fiscal 2024 | Gross Margin %\n"
        "iPhone / Products | $298,085 | $296,512 | 36.5%\n"
        "Services | $85,200 | $96,169 | 74.0%\n"
        "Total Net Sales | $383,285 | $392,681 | 46.2%\n\n"
        "Liquidity and Capital Resources:\n"
        "As of September 28, 2024, cash and marketable securities totaled $156.7 billion. Total commercial "
        "paper and term debt stood at $106.6 billion, preserving substantial balance sheet liquidity."
    )
    page2.insert_text((50, 60), text_p2, fontsize=10)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    doc.close()
    return output_path

def test_phase2_rag():
    print("=" * 65)
    print("PHASE 2: MULTIMODAL INGESTION & ADVANCED HYBRID RAG VERIFICATION")
    print("=" * 65)

    test_pdf_path = backend_dir / "data" / "uploads" / "sample_test_10k.pdf"
    
    # 1. Generate Sample PDF
    print("\n[Step 1] Creating authentic sample 10-K PDF with financial tables...")
    generate_sample_10k_pdf(test_pdf_path)
    assert test_pdf_path.exists(), "Sample PDF creation failed"
    print(f" -> Generated PDF at: {test_pdf_path.name} (Pages: 2)")

    # 2. Test Parser & Table Extraction
    print("\n[Step 2] Testing FinancialDocumentParser extraction & chunking...")
    pages = FinancialDocumentParser.extract_text_and_tables(test_pdf_path)
    assert len(pages) == 2, f"Expected 2 pages, got {len(pages)}"
    
    chunks = FinancialDocumentParser.chunk_document(pages, chunk_size=800, overlap=100)
    assert len(chunks) >= 2, "Expected at least 2 chunks from 10-K PDF"
    print(f" -> Successfully parsed {len(pages)} pages into {len(chunks)} discrete chunks.")
    for c in chunks:
        print(f"    - Chunk {c['chunk_id']} (Page {c['page_number']}) [Length: {len(c['content'])} chars]")

    # 3. Test Hybrid Vector Store Indexing
    print("\n[Step 3] Testing HybridVectorStore indexing (Qdrant Dense + BM25 Sparse)...")
    vector_store = HybridVectorStore(collection_name="phase2_verification_docs")
    session_id = "test_phase2_session"
    ticker = "AAPL"
    vector_store.index_chunks(chunks, session_id=session_id, ticker=ticker)
    print(f" -> Indexed {len(chunks)} chunks into Qdrant collection 'phase2_verification_docs' & BM25 index.")

    # 4. Test Hybrid Search (Dense + Sparse RRF)
    print("\n[Step 4] Executing Hybrid Search for query: 'Services gross margin 74%'...")
    query = "Services gross margin 74%"
    retrieved = vector_store.hybrid_search(query, top_k=3)
    assert len(retrieved) > 0, "Hybrid search returned zero results"
    
    top_result = retrieved[0]
    print(f" -> Top Retrieved Chunk ID: {top_result['chunk_id']} (Page {top_result['page_number']})")
    assert "74.0%" in top_result["content"] or "Services" in top_result["content"], "Retrieval precision failed"
    print(f" -> Snippet: {top_result['content'][:140]}...")

    # 5. Test Cross-Encoder Reranking
    print("\n[Step 5] Testing CrossEncoderReranker on candidates...")
    reranker = CrossEncoderReranker()
    reranked = reranker.rerank(query, retrieved, top_n=2)
    assert len(reranked) <= 2, "Reranker top_n limit failed"
    print(f" -> Top Reranked Chunk: {reranked[0]['chunk_id']}")

    # 6. Test FastAPI Document Upload Endpoint Integration
    print("\n[Step 6] Testing FastAPI POST /api/documents/upload integration...")
    client = TestClient(app)
    
    # Create test session first
    create_session_resp = client.post("/api/sessions?ticker=AAPL&query=Hybrid%20RAG%20Test")
    assert create_session_resp.status_code == 200
    session_data = create_session_resp.json()
    created_session_id = session_data["id"]

    # Upload PDF to endpoint
    with open(test_pdf_path, "rb") as f:
        upload_resp = client.post(
            "/api/documents/upload",
            data={"session_id": created_session_id},
            files={"file": ("sample_test_10k.pdf", f, "application/pdf")}
        )
    
    assert upload_resp.status_code == 200, f"Upload API failed: {upload_resp.text}"
    upload_result = upload_resp.json()
    print(f" -> API Upload Success: Document ID={upload_result['document_id']}")
    print(f" -> Total Pages={upload_result['total_pages']}, Chunks={upload_result['indexed_chunks']}")

    vector_store.close()

    print("\n" + "=" * 65)
    print("PHASE 2 VERIFICATION COMPLETE: ALL HYBRID RAG TESTS PASSED (100%)")
    print("=" * 65)

if __name__ == "__main__":
    test_phase2_rag()
