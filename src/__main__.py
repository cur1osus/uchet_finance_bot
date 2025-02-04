import asyncio
import logging
import sys

import aioschedule
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

import utils
from bot.handlers import setup_message_routers
from bot.middlewares import (
    CheckUser,
    DBSessionMiddleware,
    ThrottlingMiddleware,
)
from config import config
from db import Base
from init_bot import bot
from init_db import _engine, _sessionmaker
from init_db_redis import redis


async def on_startup(
    _engine: AsyncEngine,
) -> None:
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await bot.send_message(
        chat_id=config.tg_bot.developer_id,
        text="Бот запущен",
    )


async def on_shutdown(session: AsyncSession) -> None:
    await session.close_all()


async def scheduler() -> None:
    # aioschedule.every(1).seconds.do(job_sec)
    # aioschedule.every().day.at("10:30").do(any_job)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(
                command="start",
                description=await utils.get_text_message("command_start_description"),
            )
        ]
    )


async def main() -> None:
    dp = Dispatcher(_engine=_engine, storage=RedisStorage(redis=redis))

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.message.middleware(ThrottlingMiddleware())

    dp.message.middleware(DBSessionMiddleware(session_pool=_sessionmaker))
    dp.callback_query.middleware(DBSessionMiddleware(session_pool=_sessionmaker))
    dp.inline_query.middleware(DBSessionMiddleware(session_pool=_sessionmaker))
    dp.update.middleware(DBSessionMiddleware(session_pool=_sessionmaker))

    dp.message.middleware(CheckUser())
    dp.callback_query.middleware(CheckUser())
    dp.inline_query.middleware(CheckUser())

    dp.workflow_data.update({"admin_id": config.tg_bot.developer_id})

    message_routers = setup_message_routers()
    asyncio.create_task(scheduler())
    dp.include_router(message_routers)
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
