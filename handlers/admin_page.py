import sys
import os

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, input_file
from aiogram.types.input_file import FSInputFile
from keyboards import keyboard
from texts import HELLO_TEXT, points, month_names
from callbacks import Admin
import datetime as dt

router = Router()
kb = keyboard.Keyboard()


@router.message(Command("admin"))
async def cmd_start(message: Message):
    await message.answer('вы админ', reply_markup=kb.admin_kb())


@router.callback_query(Admin.filter())
async def comeback(
        call: types.CallbackQuery,
        callback_data: Admin
):
    print(callback_data)
    if callback_data.oper == 'back':
        await call.message.edit_text('вы вернулись в меню', reply_markup=kb.admin_kb())
    elif callback_data.oper == 'stops':
        point_id = 1
        await call.message.edit_text(text=f'Стоп лист для точки по адресу {points[point_id]}',
                                     reply_markup=kb.get_stops(point_id))
    elif callback_data.oper == 'zakaz':
        text, kb_ans = kb.get_waited_zakaz()
        await call.message.edit_text(text=text, reply_markup=kb_ans)
    # try:
    #     media = types.InputMediaPhoto(media=FSInputFile('media/hi.jpg'), caption=HELLO_TEXT)
    #     await call.message.edit_media(media=media, reply_markup=kb.start_kb())
    # except Exception:
    #     await call.answer_photo(
    #         photo=FSInputFile('media/hi.jpg'),
    #         caption=HELLO_TEXT,
    #         reply_markup=kb.start_kb()
    #     )
    await call.answer()
