import os

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types.input_file import FSInputFile
from keyboards import keyboard
from callbacks import *
from create_zips import *


router2 = Router()  # [2]
kb = keyboard.Keyboard()


@router2.callback_query(AdminFunc.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery,
        callback_data: AdminFunc
):
    data = callback_data
    try:
        if data.operation == 1:
            await call.message.edit_text(f"Отправялем все заказы")
        elif data.operation == 2:
            await call.message.edit_text(f"отправляем новые")
        elif data.operation == 3:
            await call.message.edit_text(f"делаем поиск")
    except:
        if data.operation == 1:
            await call.message.answer(f"Отправялем все заказы")
        elif data.operation == 2:
            await call.message.answer(f"отправляем новые")
        elif data.operation == 3:
            await call.message.answer(f"делаем поиск")
    await call.answer()
