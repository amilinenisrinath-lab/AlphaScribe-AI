from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# SQLite engine configuration
connect_args = {"check_same_thread": False}
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG, connect_args=connect_args)

def init_db():
    """Create all SQLite tables if they do not exist."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """FastAPI dependency for yielding SQLite sessions."""
    with Session(engine) as session:
        yield session
