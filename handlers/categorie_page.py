from aiogram import Router, F, types
from texts import PROFILE_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
from handlers import story_page

router = Router()


@router.callback_query(Categorie.filter())
async def categorie_of_drinks(
        call: types.CallbackQuery,
        data: types.CallbackQuery.data
):
    try:
        media = types.InputMediaPhoto(media=FSInputFile(f'media/categories/{data.name}.jpg'), caption=PROFILE_TEXT)
        await call.message.edit_media(media=media, reply_markup=kb.profile())
    except Exception:
        await call.message.answer_photo(photo=FSInputFile(f'media/categories/{data.name}.jpg'),
                                        caption=PROFILE_TEXT,
                                        reply_markup=kb.profile())
    await call.answer()
