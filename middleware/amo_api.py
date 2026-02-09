from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware

from amo_api.amo_api import AmoCRMWrapper


class AmoApiMiddleware(BaseMiddleware):
    def __init__(self, amo_api: AmoCRMWrapper, amo_fields: dict) -> None:
        self._amo_api = amo_api
        self._amo_fields = amo_fields

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        data["amo_api"] = self._amo_api
        data["amo_fields"] = self._amo_fields
        return await handler(event, data)