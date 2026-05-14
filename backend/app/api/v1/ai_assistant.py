"""
AI interview assistant API routes.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    resume_data: dict[str, Any]
    profiler_data: dict[str, Any] | None = None


class ChatRequest(BaseModel):
    message: str
    history: list[dict[str, str]] | None = None
    resume_data: dict[str, Any] | None = None


class GenerateQuestionsRequest(BaseModel):
    resume_data: dict[str, Any]


class ExplainTermRequest(BaseModel):
    term: str
    context: str | None = None


router = APIRouter()


@router.post("/analyze")
async def analyze_resume(req: AnalyzeRequest) -> dict:
    """Analyze resume with AI and return structured insights."""
    from app.services.ai_service import AIService

    service = AIService()
    result = await service.analyze_resume(req.resume_data, req.profiler_data)
    return {"success": True, "data": result}


@router.post("/explain-term")
async def explain_term(req: ExplainTermRequest):
    """Explain a professional term from the resume with streaming."""
    from app.services.ai_service import AIService
    import logging
    logger = logging.getLogger(__name__)

    service = AIService()

    async def event_generator():
        try:
            async for chunk in service.explain_term_stream(req.term, req.context):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            logger.error(f"explain_term error: {e}")
            yield f"data: 错误: {str(e)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@router.post("/generate-questions")
async def generate_questions(req: GenerateQuestionsRequest):
    """Generate interview questions with streaming output."""
    from app.services.ai_service import AIService

    service = AIService()

    async def event_generator():
        async for chunk in service.generate_questions_stream(req.resume_data):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@router.post("/chat")
async def chat(req: ChatRequest):
    """Chat with AI assistant with streaming response."""
    from app.services.ai_service import AIService

    service = AIService()

    async def event_generator():
        async for chunk in service.chat_stream(req.message, req.history, req.resume_data):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
