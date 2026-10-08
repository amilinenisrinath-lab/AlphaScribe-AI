import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

class ResearchSession(SQLModel, table=True):
    __tablename__ = "research_sessions"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    ticker: str = Field(index=True)
    query: Optional[str] = Field(default=None)
    status: str = Field(default="PENDING")  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    created_at: datetime = Field(default_factory=get_utc_now)
    updated_at: datetime = Field(default_factory=get_utc_now)

    documents: List["FinancialDocument"] = Relationship(back_populates="session")
    memos: List["InvestmentMemo"] = Relationship(back_populates="session")
    logs: List["AgentAuditLog"] = Relationship(back_populates="session")


class FinancialDocument(SQLModel, table=True):
    __tablename__ = "financial_documents"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    session_id: str = Field(foreign_key="research_sessions.id", index=True)
    filename: str
    file_path: str
    file_type: str = Field(default="PDF")
    total_pages: int = Field(default=0)
    chunk_count: int = Field(default=0)
    uploaded_at: datetime = Field(default_factory=get_utc_now)

    session: Optional[ResearchSession] = Relationship(back_populates="documents")


class InvestmentMemo(SQLModel, table=True):
    __tablename__ = "investment_memos"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    session_id: str = Field(foreign_key="research_sessions.id", index=True)
    ticker: str
    title: str
    markdown_content: str
    status: str = Field(default="DRAFT")  # DRAFT, VERIFIED, REJECTED
    chart_paths_json: Optional[str] = Field(default="[]")  # Serialized list of chart URLs/paths
    citations_json: Optional[str] = Field(default="[]")    # Serialized citations mapping
    created_at: datetime = Field(default_factory=get_utc_now)

    session: Optional[ResearchSession] = Relationship(back_populates="memos")


class AgentAuditLog(SQLModel, table=True):
    __tablename__ = "agent_audit_logs"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    session_id: str = Field(foreign_key="research_sessions.id", index=True)
    agent_name: str
    action: str
    details: Optional[str] = Field(default=None)
    timestamp: datetime = Field(default_factory=get_utc_now)

    session: Optional[ResearchSession] = Relationship(back_populates="logs")
