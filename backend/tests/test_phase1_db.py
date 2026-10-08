"""
Phase 1 Verification Script: SQLite Database & SQLModel Schema Testing
Verifies database initialization, table creation, relationships, and CRUD operations.
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from sqlmodel import Session, select
from app.db.session import engine, init_db
from app.db.models import ResearchSession, FinancialDocument, InvestmentMemo, AgentAuditLog

def test_phase1_database():
    print("=" * 60)
    print("PHASE 1: SQLITE DATABASE & ORM VERIFICATION")
    print("=" * 60)

    # 1. Initialize schema
    print("\n[Step 1] Initializing SQLite database schema...")
    init_db()
    print(" -> SQLite tables created successfully.")

    with Session(engine) as session:
        # 2. Test Session Creation
        print("\n[Step 2] Testing ResearchSession creation...")
        test_session = ResearchSession(
            ticker="NVDA",
            query="Analyze Data Center compute revenue trajectory and GPU margins.",
            status="IN_PROGRESS"
        )
        session.add(test_session)
        session.commit()
        session.refresh(test_session)
        print(f" -> Created session: ID={test_session.id}, Ticker={test_session.ticker}, Status={test_session.status}")

        # 3. Test FinancialDocument Record
        print("\n[Step 3] Testing FinancialDocument attachment...")
        test_doc = FinancialDocument(
            session_id=test_session.id,
            filename="nvda-2026-10k.pdf",
            file_path="/app/data/uploads/nvda-2026-10k.pdf",
            total_pages=112,
            chunk_count=248
        )
        session.add(test_doc)
        session.commit()
        print(f" -> Attached document: {test_doc.filename} ({test_doc.chunk_count} chunks)")

        # 4. Test InvestmentMemo Record
        print("\n[Step 4] Testing InvestmentMemo persistence...")
        test_memo = InvestmentMemo(
            session_id=test_session.id,
            ticker="NVDA",
            title="Institutional Investment Memo: NVDA",
            markdown_content="# NVDA Investment Memo\n\nData Center revenue expanded by 150% YoY.",
            status="VERIFIED",
            chart_paths_json='["/outputs/nvda_revenue_trend.png"]',
            citations_json='[{"key": "[SEC-Doc-1]", "page": 42}]'
        )
        session.add(test_memo)
        session.commit()
        print(f" -> Stored memo: {test_memo.title} (Status: {test_memo.status})")

        # 5. Test AgentAuditLog Record
        print("\n[Step 5] Testing AgentAuditLog tracking...")
        test_log = AgentAuditLog(
            session_id=test_session.id,
            agent_name="Fact-Checker",
            action="VERIFICATION_PASSED",
            details="All 8 numerical claims validated against SEC 10-K tables."
        )
        session.add(test_log)
        session.commit()
        print(f" -> Recorded audit log: Agent={test_log.agent_name}, Action={test_log.action}")

        # 6. Verify Relationships & Querying
        print("\n[Step 6] Verifying ORM query relationships...")
        queried_session = session.exec(
            select(ResearchSession).where(ResearchSession.id == test_session.id)
        ).first()

        assert queried_session is not None, "Session query failed"
        assert len(queried_session.documents) == 1, "Document relationship mismatch"
        assert len(queried_session.memos) == 1, "Memo relationship mismatch"
        assert len(queried_session.logs) == 1, "Audit log relationship mismatch"

        print(f" -> Verification passed! Linked documents: {len(queried_session.documents)}")
        print(f" -> Linked memos: {len(queried_session.memos)}")
        print(f" -> Linked logs: {len(queried_session.logs)}")

    print("\n" + "=" * 60)
    print("PHASE 1 VERIFICATION COMPLETE: ALL TESTS PASSED (100%)")
    print("=" * 60)

if __name__ == "__main__":
    test_phase1_database()
