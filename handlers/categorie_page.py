from aiogram import Router, F, types
from texts import PROFILE_TEXT, CATEGORIES_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
from handlers import story_page

router = Router()


@router.callback_query(Categories.filter())
async def categorie_of_drinks(
        call: types.CallbackQuery,
        callback_data:Categories
):

    try:
        media = types.InputMediaPhoto(media=FSInputFile(f'media/categorie/{callback_data.name}.png'), caption=CATEGORIES_TEXT[callback_data.name])
        await call.message.edit_media(media=media, reply_markup=kb.categories(callback_data.name))
    except Exception:
        await call.message.answer_photo(photo=FSInputFile(f'media/categorie/{callback_data.name}.png'),
                                        caption=CATEGORIES_TEXT[callback_data.name],
                                        reply_markup=kb.categories(callback_data.name))
    await call.answer()
