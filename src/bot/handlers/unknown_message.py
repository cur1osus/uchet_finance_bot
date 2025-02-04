from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils import (
    get_text_message,
)

router = Router()
flags = {"throttling_key": "default"}


@router.message()
async def any_unknown_message(message: Message, state: FSMContext) -> None:
    await message.answer(text=await get_text_message("answer_on_unknown_message"))
    # print(message.effect_id)


@router.callback_query()
async def any_unknown_callback(query: CallbackQuery) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
