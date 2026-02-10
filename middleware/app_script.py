from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiohttp import ClientSession, ClientTimeout


logger = logging.getLogger(__name__)


class AppScriptClient:
    def __init__(self, token: str, webhook_url: str | None, timeout_seconds: int = 10) -> None:
        self._webhook_url = webhook_url or ""
        self._timeout = ClientTimeout(total=timeout_seconds)
        self.token: str = token

    async def send(self, payload: dict[str, Any]) -> bool:
        if not self._webhook_url:
            logger.warning("App Script URL is not configured. Payload is not sent.")
            return False
        payload["token"] = self.token
        async with ClientSession(timeout=self._timeout) as session:
            async with session.post(self._webhook_url, json=payload) as response:
                if response.status >= 400:
                    body = await response.text()
                    logger.error(
                        "App Script request failed: status=%s body=%s",
                        response.status,
                        body,
                    )
                    return False
                return True


class AppScriptMiddleware(BaseMiddleware):
    def __init__(self, app_script: AppScriptClient) -> None:
        self._app_script = app_script

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        data["app_script"] = self._app_script
        return await handler(event, data)
