from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Resume(Base):
    """Resume model for parsed resume data."""

    __tablename__ = "resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_name = Column(String(100), nullable=False)
    candidate_email = Column(String(255), nullable=True)
    candidate_phone = Column(String(50), nullable=True)
    file_path = Column(String(500), nullable=False)
    raw_content = Column(Text, nullable=True)
    parsed_data = Column(JSONB, default=dict)
    status = Column(String(50), default="pending")  # pending, parsed, analyzed, error
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    skills = relationship("ResumeSkill", back_populates="resume", cascade="all, delete-orphan")
    experiences = relationship("ResumeExperience", back_populates="resume", cascade="all, delete-orphan")


class ResumeSkill(Base):
    """Resume skill model."""

    __tablename__ = "resume_skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    proficiency = Column(String(50), nullable=True)  # beginner, intermediate, advanced, expert
    years_experience = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    resume = relationship("Resume", back_populates="skills")


class ResumeExperience(Base):
    """Resume work experience model."""

    __tablename__ = "resume_experiences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    company = Column(String(200), nullable=False)
    title = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_current = Column(String(10), default="false")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    resume = relationship("Resume", back_populates="experiences")
