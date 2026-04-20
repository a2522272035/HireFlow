from __future__ import annotations

from typing import Annotated, Any

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """Global state schema for LangGraph agents."""

    # Messages history
    messages: Annotated[list, add_messages]

    # Resume data
    resume_id: str | None
    resume_content: dict[str, Any] | None
    resume_gaps: list[dict[str, Any]] | None

    # Interview data
    interview_id: str | None
    current_question: str | None
    candidate_answer: str | None
    credibility_score: float | None

    # Report data
    report_id: str | None
    evaluation_summary: str | None
    recommendations: list[str] | None

    # RAG data
    policy_query: str | None
    retrieved_documents: list[dict[str, Any]] | None

    # Metadata
    step: str
    error: str | None
