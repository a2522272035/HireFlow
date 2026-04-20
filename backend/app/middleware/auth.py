from __future__ import annotations

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

security = HTTPBearer()


class AuthMiddleware:
    """Authentication middleware."""

    async def __call__(self, request: Request, call_next):
        """Process request and check authentication."""
        # TODO: Implement JWT authentication
        # TODO: Skip auth for public endpoints
        response = await call_next(request)
        return response


async def verify_token(request: Request) -> dict:
    """Verify JWT token from request."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    # TODO: Implement token verification
    return {}
