from aiogram import Router, F, types
from texts import CONTACT_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb


router = Router()


@router.callback_query(Contacts.filter())
async def open_contacts(
        call: types.CallbackQuery
):
    chat_id = call.from_user.id
    try:
        media = types.InputMediaPhoto(media=FSInputFile('media/contact.jpeg'), caption=CONTACT_TEXT(chat_id))
        await call.message.edit_media(media=media, reply_markup=kb.contact())
    except Exception:
        await call.message.answer_photo(photo=FSInputFile('media/contact.jpeg'),
                                        caption=CONTACT_TEXT(chat_id),
                                        reply_markup=kb.contact())
    await call.answer()
