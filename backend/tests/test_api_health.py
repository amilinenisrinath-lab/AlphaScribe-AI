"""
FastAPI Server & Health Endpoint Test
"""

import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from starlette.testclient import TestClient
from app.main import app

def test_api():
    print("Testing FastAPI Application & Lifespan...")
    client = TestClient(app)

    # 1. Test Root
    res_root = client.get("/")
    print(f"GET / -> Status {res_root.status_code}: {res_root.json()}")
    assert res_root.status_code == 200

    # 2. Test Health
    res_health = client.get("/health")
    print(f"GET /health -> Status {res_health.status_code}: {res_health.json()}")
    assert res_health.status_code == 200
    assert res_health.json()["project"] == "AlphaScribe AI"
    assert res_health.json()["database"] == "SQLite (Connected)"

    # 3. Test Session Creation endpoint
    res_session = client.post("/api/sessions?ticker=AAPL&query=Test%20Query")
    print(f"POST /api/sessions -> Status {res_session.status_code}: {res_session.json()}")
    assert res_session.status_code == 200
    assert res_session.json()["ticker"] == "AAPL"

    print("\nAPI HEALTH & ROUTING VERIFIED SUCCESSFULLY (100% OK)!")

if __name__ == "__main__":
    test_api()
