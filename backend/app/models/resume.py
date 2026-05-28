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
    name = Column(String(100), nullable=True)
    original_filename = Column(String(500), nullable=True)
    file_type = Column(String(50), nullable=True)
    candidate_name = Column(String(100), nullable=False)
    candidate_email = Column(String(255), nullable=True)
    candidate_phone = Column(String(50), nullable=True)
    candidate_gender = Column(String(20), nullable=True)
    candidate_age = Column(Integer, nullable=True)
    candidate_location = Column(String(100), nullable=True)
    file_path = Column(String(500), nullable=False)
    candidate_id = Column(String(100), nullable=True)
    candidate_fingerprint = Column(String(128), nullable=True)
    school = Column(String(200), nullable=True)
    degree = Column(String(100), nullable=True)
    major = Column(String(200), nullable=True)
    work_year = Column(String(50), nullable=True)
    current_position = Column(String(200), nullable=True)
    current_company = Column(String(200), nullable=True)
    expect_job = Column(String(200), nullable=True)
    expect_salary = Column(String(100), nullable=True)
    resume_integrity = Column(String(50), nullable=True)
    file_name = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)
    file_sha256 = Column(String(64), nullable=True)
    content_sha256 = Column(String(64), nullable=True)
    raw_content = Column(Text, nullable=True)
    parsed_data = Column(JSONB, default=dict)
    parsed_json = Column(JSONB, default=dict)
    raw_sdk_response = Column(JSONB, default=dict)
    parsed_text = Column(Text, nullable=True)
    parser_name = Column(String(50), default="resumesdk")
    parser_version = Column(String(50), nullable=True)
    parsed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="pending")  # pending, parsed, analyzed, error
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
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
    skill = Column(String(100), nullable=True)
    skill_name = Column(String(100), nullable=False)
    proficiency = Column(String(50), nullable=True)  # beginner, intermediate, advanced, expert
    years_of_experience = Column(Integer, nullable=True)
    years_experience = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    resume = relationship("Resume", back_populates="skills")


class ResumeExperience(Base):
    """Resume work experience model."""

    __tablename__ = "resume_experiences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    company = Column(String(200), nullable=False)
    position = Column(String(200), nullable=True)
    title = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_current = Column(String(10), default="false")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    resume = relationship("Resume", back_populates="experiences")
