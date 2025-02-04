from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import BlackList, User
from utils import get_text_message


class CheckUser(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        session: AsyncSession = data["session"]
        if await session.scalar(
            select(BlackList).where(BlackList.id_user == event.from_user.id)
        ):
            return
        user = await session.scalar(
            select(User).where(User.id_user == event.from_user.id)
        )
        if not user:
            user = User(
                id_user=event.from_user.id,
                username=f"@{event.from_user.username}"
                if event.from_user.username
                else "@none",
            )
            session.add(user)
            await session.commit()
        data["user"] = user
        if isinstance(event, Message) and not user:
            if (
                event.text.startswith("/start")
                or data.get("raw_state") == "UserState:start_reg_step"
            ):
                return await handler(event, data)
            return await event.answer(
                text=await get_text_message("press_start_to_play"),
                reply_markup=ReplyKeyboardRemove(),
            )
        return await handler(event, data)
