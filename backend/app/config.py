"""
config.py — Application Configuration & Environment Variables
=============================================================
Centralises all configuration loaded from environment variables or a .env file.
Uses Pydantic's BaseSettings for type-safe env parsing with defaults.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide settings, loaded from environment / .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # ── App ─────────────────────────────────────────────────────────────────
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001", "*"]

    # ── Database (PostgreSQL) ────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/sbi_agents"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # ── LLM ─────────────────────────────────────────────────────────────────
    LLM_PROVIDER: str = "local"           # "local" | "anthropic" | "openai"
    ANTHROPIC_API_KEY: str = ""           # Claude API key
    OPENAI_API_KEY: str = ""              # GPT-4 API key
    LLM_MODEL_NAME: str = "claude-3-5-sonnet-20241022"
    LLM_TEMPERATURE: float = 0.2
    LLM_MAX_TOKENS: int = 4096

    # ── Vector Store ────────────────────────────────────────────────────────
    VECTOR_STORE_PROVIDER: str = "chroma"
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
    PINECONE_API_KEY: str = ""

    # ── Voice ───────────────────────────────────────────────────────────────
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    DEEPGRAM_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""

    # ── Pipeline ────────────────────────────────────────────────────────────
    AGENT_MAX_RETRIES: int = 3
    AGENT_RETRY_BACKOFF_SECONDS: float = 2.0


settings = Settings()
