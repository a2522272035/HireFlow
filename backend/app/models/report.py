from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.database import Base


class EvaluationReport(Base):
    """Evaluation report model."""

    __tablename__ = "evaluation_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interview_id = Column(UUID(as_uuid=True), ForeignKey("interviews.id"), nullable=False)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    status = Column(String(50), default="pending")  # pending, generating, completed, error

    # Assessment scores
    technical_score = Column(Float, nullable=True)
    behavioral_score = Column(Float, nullable=True)
    credibility_score = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)

    # Report content
    executive_summary = Column(Text, nullable=True)
    strengths = Column(JSONB, default=list)
    weaknesses = Column(JSONB, default=list)
    recommendations = Column(JSONB, default=list)
    detailed_assessment = Column(JSONB, default=dict)

    # Hiring decision
    recommendation = Column(String(50), nullable=True)  # strong_hire, hire, neutral, no_hire
    confidence_level = Column(Float, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
