from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/callback")
async def verify_callback(
    msg_signature: str,
    timestamp: str,
    nonce: str,
    echostr: str,
) -> str:
    """Verify WeCom callback URL."""
    # TODO: Implement URL verification
    return echostr


@router.post("/callback")
async def handle_callback(request: Request) -> dict:
    """Handle WeCom message callback."""
    # TODO: Implement message handling
    return {"status": "ok"}


@router.post("/send")
async def send_notification(user_id: str, message: str) -> dict:
    """Send notification to WeCom user."""
    # TODO: Implement notification sending
    return {"status": "sent", "user_id": user_id}
