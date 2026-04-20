from __future__ import annotations

import time

from fastapi import Request

from app.utils.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware:
    """Request/response logging middleware."""

    async def __call__(self, request: Request, call_next):
        """Log request and response details."""
        start_time = time.time()

        # Log request
        logger.info(
            "Request started",
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else None,
        )

        response = await call_next(request)

        # Log response
        duration = time.time() - start_time
        logger.info(
            "Request completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2),
        )

        return response
