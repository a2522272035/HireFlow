from __future__ import annotations

from typing import Any

from app.agents.state import AgentState


class RealtimeSuggester:
    """Agent for real-time interview suggestions."""

    async def suggest_follow_up(
        self,
        transcript: list[dict[str, Any]],
        context: dict[str, Any],
    ) -> str | None:
        """Suggest follow-up question based on conversation."""
        # TODO: Implement real-time suggestion
        # TODO: Analyze transcript and suggest next question
        return None

    async def detect_clarification_needed(
        self,
        answer: str,
    ) -> bool:
        """Detect if clarification is needed."""
        # TODO: Implement clarification detection
        return False


def realtime_suggester_node(state: AgentState) -> AgentState:
    """LangGraph node for real-time suggestions."""
    # TODO: Implement node logic
    return state
