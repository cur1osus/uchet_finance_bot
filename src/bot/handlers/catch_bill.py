import os
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_text_message, read_qr_from_image
from db import Bill, Product

from utils import get_text_message, StringQr, get_dict_products

router = Router()
flags = {"throttling_key": "default"}


@router.message(F.content_type == "photo")
async def photo_catch(message: Message, session: AsyncSession) -> None:
    # save file
    photo_id = message.photo[-1].file_id
    file = await message.bot.get_file(photo_id)
    file_path = file.file_path
    file_name = f"qrcode_{message.from_user.id}.jpg"
    await message.bot.download_file(file_path, file_name)

    string_from_qr = read_qr_from_image(file_name)
    fp, fn, fd = StringQr.get_fp_fn_fd(string_from_qr)
    bill = Bill(
        fp=fp,
        fn=fn,
        fd=fd,
        date=StringQr.get_format_time(string_from_qr),
        sum=StringQr.get_sum(string_from_qr),
    )
    session.add(bill)
    await session.flush()
    products = get_dict_products(string_from_qr)["items"]
    for product in products:
        product = Product(
            idpk_bill=bill.idpk,
            name=product["name"],
            price=product["price"],
            count=product["count"],
            sum=product["sum"],
        )
        session.add(product)
    await session.commit()
    os.remove(file_name)
    await message.answer(text=await get_text_message("bill_added"))
