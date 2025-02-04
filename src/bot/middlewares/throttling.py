from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, CallbackQuery
from cachetools import TTLCache

THROTTLE_TIME = 0.5


class ThrottlingMiddleware(BaseMiddleware):
    caches = {"default": TTLCache(maxsize=10_000, ttl=THROTTLE_TIME)}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        throttling_key = get_flag(data, "throttling_key")
        if throttling_key is not None:
            cache = self.caches.get(throttling_key)
            if cache is not None:
                cache[event.chat.id] = None
            else:
                if isinstance(event, CallbackQuery):
                    await event.answer("⏳ Too fast!", show_alert=True)
                return

        return await handler(event, data)
