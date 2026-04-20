from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/ws/asr/{interview_id}")
async def asr_websocket(websocket: WebSocket, interview_id: str):
    """WebSocket endpoint for real-time ASR."""
    await websocket.accept()

    try:
        while True:
            # Receive audio data
            audio_data = await websocket.receive_bytes()

            # TODO: Process audio with ASR engine
            # TODO: Send transcription result
            await websocket.send_json({
                "type": "transcription",
                "text": "",
                "is_final": False,
            })

    except WebSocketDisconnect:
        # Handle disconnection
        pass
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e),
        })
        await websocket.close()
