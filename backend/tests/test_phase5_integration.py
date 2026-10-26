"""
Phase 5 Verification Test Suite: FastAPI REST & SSE Streaming Full-Stack Integration
Tests:
1. End-to-end session creation.
2. Document upload and hybrid indexing pipeline.
3. Real-time Server-Sent Events (SSE) streaming (/api/analyze/stream).
4. Verification of agent step notifications and final payload tokens.
5. Memo retrieval from SQLite via GET /api/memos/{memo_id}.
6. Static chart image asset serving via GET /api/outputs/{filename}.
"""

import sys
import json
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

import fitz
from starlette.testclient import TestClient
from app.main import app

def generate_test_pdf(file_path: Path):
    """Generates a small test PDF for integration tests."""
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text(
        (50, 60),
        "Item 7. Management Discussion and Analysis\n"
        "Services revenue reached $96.2 billion with 74.0% gross margin.\n"
        "Capital expenditures totaled $11.5 billion.",
        fontsize=10
    )
    file_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(file_path)
    doc.close()

def test_phase5_integration():
    print("=" * 65)
    print("PHASE 5: FASTAPI REST & SSE STREAMING INTEGRATION VERIFICATION")
    print("=" * 65)

    client = TestClient(app)

    # 1. Test Session Creation
    print("\n[Step 1] Creating Research Session via POST /api/sessions...")
    session_res = client.post("/api/sessions?ticker=AAPL&query=Integration%20Test%20Query")
    assert session_res.status_code == 200, f"Session creation failed: {session_res.text}"
    session_data = session_res.json()
    session_id = session_data["id"]
    print(f" -> Session created: ID={session_id}, Ticker={session_data['ticker']}, Status={session_data['status']}")

    # 2. Test Document Upload Endpoint
    print("\n[Step 2] Testing Document Upload via POST /api/documents/upload...")
    pdf_path = backend_dir / "data" / "uploads" / f"{session_id}_test.pdf"
    generate_test_pdf(pdf_path)

    with open(pdf_path, "rb") as f:
        upload_res = client.post(
            "/api/documents/upload",
            data={"session_id": session_id},
            files={"file": ("integration_test.pdf", f, "application/pdf")}
        )
    assert upload_res.status_code == 200, f"Upload failed: {upload_res.text}"
    upload_data = upload_res.json()
    print(f" -> Document Uploaded: ID={upload_data['document_id']}, Indexed Chunks={upload_data['indexed_chunks']}")

    # 3. Test Real-Time SSE Stream Endpoint (/api/analyze/stream)
    print("\n[Step 3] Connecting to SSE Stream via GET /api/analyze/stream...")
    stream_url = f"/api/analyze/stream?session_id={session_id}&ticker=AAPL&query=Analyze%20Services%20margins"
    
    events_received = []
    final_memo_id = None
    final_chart_url = None

    with client.stream("GET", stream_url) as response:
        assert response.status_code == 200, f"Stream connection failed: {response.status_code}"
        
        for line in response.iter_lines():
            line_str = line.strip()
            if line_str.startswith("data:"):
                payload_str = line_str[len("data:"):].strip()
                event_data = json.loads(payload_str)
                event_type = event_data.get("event")
                events_received.append(event_type)

                if event_type == "start":
                    print(f" -> [SSE Event: START] {event_data.get('message')}")
                elif event_type == "agent_step":
                    print(f" -> [SSE Event: STEP] Agent [{event_data.get('node').upper()}]: {event_data.get('message')}")
                elif event_type == "complete":
                    final_memo_id = event_data.get("memo_id")
                    final_chart_url = event_data.get("chart_url")
                    print(f" -> [SSE Event: COMPLETE] Memo ID={final_memo_id}, Chart URL={final_chart_url}")

    assert "start" in events_received, "Missing start event in SSE stream"
    assert "agent_step" in events_received, "Missing agent_step events in SSE stream"
    assert "complete" in events_received, "Missing complete event in SSE stream"
    assert final_memo_id is not None, "Complete event missing memo_id"
    print(f" -> Stream executed successfully! Total events received: {len(events_received)}")

    # 4. Test Memo Retrieval from SQLite (GET /api/memos/{memo_id})
    print("\n[Step 4] Retrieving Persisted Memo via GET /api/memos/{memo_id}...")
    memo_res = client.get(f"/api/memos/{final_memo_id}")
    assert memo_res.status_code == 200, f"Memo retrieval failed: {memo_res.text}"
    memo_data = memo_res.json()
    assert memo_data["ticker"] == "AAPL"
    assert memo_data["status"] == "VERIFIED"
    assert len(memo_data["markdown_content"]) > 300
    print(f" -> Retrieved Memo: Title='{memo_data['title']}' (Status: {memo_data['status']})")
    print(f" -> Stored Content Length: {len(memo_data['markdown_content'])} characters")

    # 5. Test Chart Serving Endpoint (GET /api/outputs/{filename})
    if final_chart_url:
        print("\n[Step 5] Testing Chart Asset Serving via GET /outputs/...")
        chart_res = client.get(final_chart_url)
        assert chart_res.status_code == 200, f"Chart image serving failed: {chart_res.status_code}"
        assert len(chart_res.content) > 1000, "Served chart content is empty"
        print(f" -> Successfully served chart image asset ({len(chart_res.content):,} bytes)")

    print("\n" + "=" * 65)
    print("PHASE 5 VERIFICATION COMPLETE: ALL INTEGRATION TESTS PASSED (100%)")
    print("=" * 65)

if __name__ == "__main__":
    test_phase5_integration()
