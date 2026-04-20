"""Database initialization script."""

from __future__ import annotations

import asyncio

from app.core.database import engine
from app.models import Base


async def init_database() -> None:
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_database())
