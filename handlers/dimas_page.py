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


@router2.callback_query(DimasFunc.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery,
        callback_data: DimasFunc
):
    data = callback_data
    try:
        if data.operation == 1:
            await call.message.edit_text(f"Отправялем бд, которая sqlite")
        elif data.operation == 2:
            await call.message.edit_text(f"Жди, архивы уже формируются")
            make_zips()
            await call.message.answer('Архивы сформировались, начинаю отправлять')
            for i in os.listdir('zips'):
                await call.message.answer_document(FSInputFile('zips/'+i))
    except:
        if data.operation == 1:
            await call.message.answer(f"Отправялем бд, которая sqlite")
        elif data.operation == 2:
            await call.message.edit_text(f"Жди, архивы уже формируются")
            make_zips()
            await call.message.answer('Архивы сформировались, начинаю отправлять')
            for i in os.listdir('zips'):
                await call.message.answer_document(FSInputFile('zips/'+i))
    await call.answer()
