from aiogram import Router, F, types
from texts import PROFILE_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
from handlers import story_page

router = Router()


@router.callback_query(Busket.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery,
        callback_data: Busket

):
    if callback_data.back == 'menu':
        print('корзина')
    elif callback_data.back == 'categorie':
        print('категория')
    else:
        await call.message.edit_caption('текст для корзины', reply_markup=kb.busket(int(callback_data.drink_id)))
    await call.answer()

