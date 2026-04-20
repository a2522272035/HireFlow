from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Interview(Base):
    """Interview session model."""

    __tablename__ = "interviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    interviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="scheduled")  # scheduled, in_progress, completed, cancelled
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    overall_score = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    meta_data = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    messages = relationship("InterviewMessage", back_populates="interview", cascade="all, delete-orphan")


class InterviewMessage(Base):
    """Interview message/dialog model."""

    __tablename__ = "interview_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interview_id = Column(UUID(as_uuid=True), ForeignKey("interviews.id"), nullable=False)
    role = Column(String(50), nullable=False)  # interviewer, candidate, system
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default="text")  # text, question, answer, suggestion
    credibility_score = Column(Float, nullable=True)
    meta_data = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    interview = relationship("Interview", back_populates="messages")
