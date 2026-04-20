from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReportBase(BaseModel):
    """Base schema for evaluation report."""

    interview_id: UUID
    resume_id: UUID


class ReportCreate(ReportBase):
    """Schema for creating report."""

    pass


class ReportResponse(ReportBase):
    """Schema for report response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    technical_score: float | None
    behavioral_score: float | None
    credibility_score: float | None
    overall_score: float | None
    executive_summary: str | None
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    detailed_assessment: dict[str, Any]
    recommendation: str | None
    confidence_level: float | None
    created_at: datetime
    updated_at: datetime


class ReportGenerateRequest(BaseModel):
    """Schema for report generation request."""

    interview_id: UUID


class ReportListItem(BaseModel):
    """Schema for report list item."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    interview_id: UUID
    candidate_name: str
    overall_score: float | None
    recommendation: str | None
    created_at: datetime
