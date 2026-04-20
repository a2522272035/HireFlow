from __future__ import annotations

import httpx

from app.config import settings


class WeComService:
    """WeCom (Enterprise WeChat) API service."""

    BASE_URL = "https://qyapi.weixin.qq.com/cgi-bin"

    def __init__(self) -> None:
        self.corp_id = settings.WECOM_CORP_ID
        self.agent_id = settings.WECOM_AGENT_ID
        self.secret = settings.WECOM_SECRET
        self._access_token: str | None = None

    async def _get_access_token(self) -> str | None:
        """Get WeCom access token."""
        if self._access_token:
            return self._access_token

        if not self.corp_id or not self.secret:
            return None

        url = f"{self.BASE_URL}/gettoken"
        params = {
            "corpid": self.corp_id,
            "corpsecret": self.secret,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()

            if data.get("errcode") == 0:
                self._access_token = data["access_token"]
                return self._access_token

        return None

    async def send_message(
        self,
        user_id: str,
        message: str,
    ) -> bool:
        """Send text message to user."""
        access_token = await self._get_access_token()
        if not access_token:
            return False

        url = f"{self.BASE_URL}/message/send"
        params = {"access_token": access_token}
        payload = {
            "touser": user_id,
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {"content": message},
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, params=params, json=payload)
            data = response.json()
            return data.get("errcode") == 0

    async def update_smart_sheet(
        self,
        sheet_id: str,
        data: dict,
    ) -> bool:
        """Update smart sheet (智能表格)."""
        # TODO: Implement smart sheet update
        # Reference: https://developer.work.weixin.qq.com/document/path/97484
        return True


# Global WeCom service instance
wecom_service = WeComService()
