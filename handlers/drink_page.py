from aiogram import Router, F, types
from texts import PROFILE_TEXT, CATEGORIES_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
from handlers import story_page

router = Router()


@router.callback_query(Drink.filter())
async def drink(
        call: types.CallbackQuery,
        callback_data: Drink
):
    photo_name = kb.sql.execute(
        f"SELECT photo FROM menu WHERE type='{callback_data.categorie}' AND name='{callback_data.name}'").fetchone()[0]
    desk = kb.sql.execute(
        f"SELECT desk FROM menu WHERE type='{callback_data.categorie}' AND name='{callback_data.name}'").fetchone()[0]
    price = str(kb.sql.execute(
        f"SELECT cost FROM menu WHERE type='{callback_data.categorie}' AND name='{callback_data.name}'").fetchone()[0])
    desk += '\n'+f'<b>{price}</b> ₽'
    try:
        media = types.InputMediaPhoto(media=FSInputFile(f'media/drinks/{photo_name}'),
                                      caption=desk)
        await call.message.edit_media(media=media, reply_markup=kb.drink_kb(callback_data.name,callback_data.categorie))
    except Exception:
        await call.message.answer_photo(photo=FSInputFile(f'media/drinks/{photo_name}'),
                                        caption=desk,
                                        reply_markup=kb.drink_kb(callback_data.name,callback_data.categorie))
    await call.answer()
