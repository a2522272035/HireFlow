from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_reports() -> dict:
    """List all evaluation reports."""
    # TODO: Implement report listing
    return {"reports": []}


@router.get("/{report_id}")
async def get_report(report_id: str) -> dict:
    """Get evaluation report by ID."""
    # TODO: Implement report retrieval
    return {"report_id": report_id}


@router.post("/generate/{interview_id}")
async def generate_report(interview_id: str) -> dict:
    """Generate evaluation report for interview."""
    # TODO: Implement report generation
    return {"interview_id": interview_id, "report_id": "", "status": "pending"}
