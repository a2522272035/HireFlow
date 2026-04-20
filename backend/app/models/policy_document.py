from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID, VECTOR

from app.core.database import Base


class PolicyDocument(Base):
    """Policy document model with vector embeddings."""

    __tablename__ = "policy_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)

    # Vector embedding for RAG (dimension 1536 for OpenAI embeddings)
    embedding = Column(VECTOR(1536), nullable=True)

    # Document metadata
    doc_type = Column(String(100), nullable=True)  # handbook, policy, procedure, etc.
    department = Column(String(100), nullable=True)
    version = Column(String(50), default="1.0")
    effective_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)

    # File info
    file_path = Column(String(500), nullable=True)
    file_type = Column(String(50), nullable=True)
    file_size = Column(Integer, nullable=True)

    # Additional metadata
    tags = Column(JSONB, default=list)
    meta_data = Column(JSONB, default=dict)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
