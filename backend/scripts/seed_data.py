"""Script to seed test data."""

from __future__ import annotations

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal


async def seed_users(db: AsyncSession) -> None:
    """Seed test users."""
    # TODO: Create test users
    pass


async def seed_resumes(db: AsyncSession) -> None:
    """Seed test resumes."""
    # TODO: Create test resumes
    pass


async def main() -> None:
    """Main entry point."""
    async with AsyncSessionLocal() as db:
        await seed_users(db)
        await seed_resumes(db)
        await db.commit()
        print("Test data seeded successfully.")


if __name__ == "__main__":
    asyncio.run(main())
