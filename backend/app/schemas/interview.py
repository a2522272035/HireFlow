from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class InterviewMessageBase(BaseModel):
    """Base schema for interview message."""

    role: str
    content: str
    message_type: str = "text"
    credibility_score: float | None = None
    metadata: dict[str, Any] | None = None


class InterviewMessageCreate(InterviewMessageBase):
    """Schema for creating interview message."""

    pass


class InterviewMessageResponse(InterviewMessageBase):
    """Schema for interview message response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class InterviewBase(BaseModel):
    """Base schema for interview."""

    resume_id: UUID


class InterviewCreate(InterviewBase):
    """Schema for creating interview."""

    notes: str | None = None
    metadata: dict[str, Any] | None = None


class InterviewUpdate(BaseModel):
    """Schema for updating interview."""

    status: str | None = None
    notes: str | None = None
    overall_score: float | None = None
    ended_at: datetime | None = None


class InterviewResponse(InterviewBase):
    """Schema for interview response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    interviewer_id: UUID
    status: str
    started_at: datetime | None
    ended_at: datetime | None
    overall_score: float | None
    notes: str | None
    metadata: dict[str, Any]
    messages: list[InterviewMessageResponse] = []
    created_at: datetime
    updated_at: datetime


class QuestionGenerateRequest(BaseModel):
    """Schema for question generation request."""

    focus_areas: list[str] | None = None
    num_questions: int = 5


class QuestionResponse(BaseModel):
    """Schema for generated question."""

    category: str
    question: str
    intent: str
    follow_ups: list[str]


class CredibilityAssessmentRequest(BaseModel):
    """Schema for credibility assessment request."""

    question_id: str
    answer: str


class CredibilityAssessmentResponse(BaseModel):
    """Schema for credibility assessment response."""

    score: float
    confidence: float
    indicators: list[str]
    notes: str
