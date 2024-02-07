from aiogram import Router, F, types
from texts import PROFILE_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
from handlers import story_page
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, input_file

router = Router()


@router.callback_query(Profile.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery
):
    try:
        media = types.InputMediaPhoto(media=FSInputFile('media/persona.jpeg'), caption=PROFILE_TEXT)
        await call.message.edit_media(media=media, reply_markup=kb.profile())
    except Exception:
        await call.message.answer_photo(photo=FSInputFile('media/persona.jpeg'),
                                        caption=PROFILE_TEXT,
                                        reply_markup=kb.profile())
    await call.answer()

@router.message(Command("profle"))
async def cmd_start(message: Message):
    await message.answer_photo(photo=FSInputFile('media/persona.jpeg'),
                                    caption=PROFILE_TEXT,
                                    reply_markup=kb.profile())