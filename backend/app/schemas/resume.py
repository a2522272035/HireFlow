from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ResumeSkillBase(BaseModel):
    """Base schema for resume skill."""

    skill_name: str
    proficiency: str | None = None
    years_experience: int | None = None


class ResumeSkillCreate(ResumeSkillBase):
    """Schema for creating resume skill."""

    pass


class ResumeSkillResponse(ResumeSkillBase):
    """Schema for resume skill response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class ResumeExperienceBase(BaseModel):
    """Base schema for resume experience."""

    company: str
    title: str
    start_date: datetime | None = None
    end_date: datetime | None = None
    is_current: bool = False
    description: str | None = None


class ResumeExperienceCreate(ResumeExperienceBase):
    """Schema for creating resume experience."""

    pass


class ResumeExperienceResponse(ResumeExperienceBase):
    """Schema for resume experience response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class ResumeBase(BaseModel):
    """Base schema for resume."""

    candidate_name: str
    candidate_email: str | None = None
    candidate_phone: str | None = None


class ResumeCreate(ResumeBase):
    """Schema for creating resume."""

    raw_content: str | None = None
    parsed_data: dict[str, Any] | None = None


class ResumeUpdate(BaseModel):
    """Schema for updating resume."""

    candidate_name: str | None = None
    candidate_email: str | None = None
    candidate_phone: str | None = None
    parsed_data: dict[str, Any] | None = None
    status: str | None = None


class ResumeResponse(ResumeBase):
    """Schema for resume response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    file_path: str
    status: str
    parsed_data: dict[str, Any]
    skills: list[ResumeSkillResponse] = []
    experiences: list[ResumeExperienceResponse] = []
    created_at: datetime
    updated_at: datetime


class ResumeGapAnalysis(BaseModel):
    """Schema for resume gap analysis."""

    gaps: list[dict[str, Any]]
    suggestions: list[str]
