from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AlphaScribe AI"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = f"sqlite:///{(BASE_DIR / 'data' / 'app.db').as_posix()}"

    # API Keys
    OPENAI_API_KEY: str = ""
    
    # Qdrant Vector Store
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_LOCATION: str = str(BASE_DIR / "data" / "qdrant_storage")
    
    # Paths
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    OUTPUT_DIR: Path = BASE_DIR / "data" / "outputs"
    RSCRIPTS_DIR: Path = BASE_DIR / "r_scripts"
    RSCRIPT_PATH: str = "Rscript"

    # LangSmith Observability
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "financial-analyst-agent"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# Ensure directories exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
