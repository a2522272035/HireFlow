from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post("/upload")
async def upload_policy_document() -> dict:
    """Upload policy document for RAG."""
    # TODO: Implement document upload and indexing
    return {"message": "Document uploaded"}


@router.post("/query")
async def query_policy(query: str) -> dict:
    """Query policy documents using RAG."""
    # TODO: Implement RAG query
    return {"query": query, "answer": "", "sources": []}


@router.get("/documents")
async def list_documents() -> dict:
    """List all uploaded policy documents."""
    # TODO: Implement document listing
    return {"documents": []}
