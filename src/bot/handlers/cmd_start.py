from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db import User
from utils import (
    get_text_message,
)

router = Router()


@router.message(CommandStart())
async def command_start(
    message: Message,
    command: CommandObject,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    await message.answer(text=await get_text_message("command_start"))
