"""
database.py — Async Database Engine & Session Management
========================================================
Configures SQLAlchemy asynchronous database connectivity and session pooling.
Supports PostgreSQL (via asyncpg) and falls back to SQLite (via aiosqlite)
for seamless local development.
"""

from __future__ import annotations

import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import settings
from app.db.models import Base

logger = logging.getLogger("sbi.db")

# Automatically fallback to local SQLite if postgres isn't reachable / configured
db_url = settings.DATABASE_URL
if "postgresql" in db_url and settings.APP_ENV in ["development", "testing"]:
    # Check if a postgres daemon is likely unreachable, or use SQLite as default
    # For robust local dev, we will override default PG url with SQLite if it's the default credentials
    if "user:password" in db_url or "postgres:password" in db_url:
        logger.warning("Default PostgreSQL credentials detected. Falling back to local SQLite: sqlite+aiosqlite:///sbi_agents.db")
        db_url = "sqlite+aiosqlite:///sbi_agents.db"

# Create async engine
engine = create_async_engine(
    db_url,
    pool_pre_ping=True,
    future=True,
    # SQLite doesn't support pool_size or max_overflow arguments
    **({
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
    } if "sqlite" not in db_url else {})
)

# Async session maker
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def init_db() -> None:
    """
    Initialises the database tables. Creates all tables defined in models.py
    if they do not already exist.
    """
    logger.info(f"Initializing database at: {db_url}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized successfully.")


async def close_db() -> None:
    """
    Gracefully shuts down the database engine connection pool.
    """
    logger.info("Closing database connection pool...")
    await engine.dispose()
    logger.info("Database connection pool closed.")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency yielding a transactional async database session.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
