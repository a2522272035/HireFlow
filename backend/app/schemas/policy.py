from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PolicyDocumentBase(BaseModel):
    """Base schema for policy document."""

    title: str
    content: str
    summary: str | None = None
    doc_type: str | None = None
    department: str | None = None
    version: str = "1.0"
    effective_date: datetime | None = None
    expiry_date: datetime | None = None
    tags: list[str] | None = None


class PolicyDocumentCreate(PolicyDocumentBase):
    """Schema for creating policy document."""

    pass


class PolicyDocumentUpdate(BaseModel):
    """Schema for updating policy document."""

    title: str | None = None
    content: str | None = None
    summary: str | None = None
    doc_type: str | None = None
    department: str | None = None
    version: str | None = None
    effective_date: datetime | None = None
    expiry_date: datetime | None = None
    tags: list[str] | None = None


class PolicyDocumentResponse(PolicyDocumentBase):
    """Schema for policy document response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    file_path: str | None
    file_type: str | None
    file_size: int | None
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class PolicyQueryRequest(BaseModel):
    """Schema for policy query request."""

    query: str
    top_k: int = 5


class PolicyQueryResponse(BaseModel):
    """Schema for policy query response."""

    query: str
    answer: str
    sources: list[dict[str, Any]]
    confidence: float


class PolicyDocumentListItem(BaseModel):
    """Schema for policy document list item."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    doc_type: str | None
    department: str | None
    version: str
    created_at: datetime
