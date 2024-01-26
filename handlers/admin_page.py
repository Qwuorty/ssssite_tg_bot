import os

from db import Datebase
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types.input_file import FSInputFile
from keyboards import keyboard
from callbacks import *
from create_zips import *


router2 = Router()  # [2]
kb = keyboard.Keyboard()
db = Datebase()

@router2.callback_query(AdminFunc.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery,
        callback_data: AdminFunc
):
    data = callback_data
    try:
        if data.operation == 1:
            arr = db.get_all_orders()

            for i in arr:
                order_id = i[0]
                mail = i[1]
                name = i[2]
                surname = i[3]
                net = i[4]
                phone = i[5]
                address = i[6]
                postcode = i[7]
                basket = [a.split(':') for a in str(i[8]).split(';')]
                date = i[9]
                status = i[10]
                cost = db.get_cost_by_basket(basket)
                text = f"""
Имя - {name}
фамилия - {surname}
почта - {mail}
контакт - {net}
стоимость - {cost}

"""
                await call.message.answer(text)
        elif data.operation == 2:
            await call.message.edit_text(f"отправляем новые")
        elif data.operation == 3:
            await call.message.edit_text(f"делаем поиск")
    except:
        if data.operation == 1:
            arr = db.get_all_orders()

            for i in arr:
                order_id = i[0]
                mail = i[1]
                name = i[2]
                surname = i[3]
                net = i[4]
                phone = i[5]
                address = i[6]
                postcode = i[7]
                basket = [a.split(':') for a in str(i[8]).split(';')]
                date = i[9]
                status = i[10]
                cost = db.get_cost_by_basket(basket)
                text = f"""
Имя - {name}
фамилия - {surname}
почта - {mail}
контакт - {net}
стоимость - {cost}

"""
                await call.message.answer(text)
        elif data.operation == 2:
            await call.message.answer(f"отправляем новые")
        elif data.operation == 3:
            await call.message.answer(f"делаем поиск")
    await call.answer()
