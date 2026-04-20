from __future__ import annotations

from typing import Any

from app.agents.state import AgentState


class QuestionGenerator:
    """Agent for generating interview questions."""

    async def generate(
        self,
        resume_data: dict[str, Any],
        gaps: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        """Generate interview questions based on resume and gaps."""
        # TODO: Implement question generation
        # TODO: Generate: technical, behavioral, gap-related questions
        return []

    async def generate_follow_up(
        self,
        previous_answer: str,
        context: dict[str, Any],
    ) -> str | None:
        """Generate follow-up question based on previous answer."""
        # TODO: Implement follow-up generation
        return None


def question_generator_node(state: AgentState) -> AgentState:
    """LangGraph node for question generation."""
    # TODO: Implement node logic
    return state
