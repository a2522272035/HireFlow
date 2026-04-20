from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class ReportService:
    """Service for report operations."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def generate_report(self, interview_id: str) -> dict[str, Any]:
        """Generate evaluation report for interview."""
        # TODO: Implement report generation
        return {}

    async def get_report(self, report_id: str) -> dict[str, Any] | None:
        """Get report by ID."""
        # TODO: Implement report retrieval
        return None

    async def list_reports(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """List all reports."""
        # TODO: Implement report listing
        return []
