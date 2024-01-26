import sys
import os

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, input_file
from aiogram.types.input_file import FSInputFile
from keyboards import keyboard
from handlers import profile_page,story_page,contact_page,menu_page
from texts import HELLO_TEXT
from callbacks import MainPage

router = Router()  #
kb = keyboard.Keyboard()
router.include_routers(profile_page.router,
                       story_page.router,
                       contact_page.router,
                       menu_page.router)


# Приветственное сообщение
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer_photo(
        photo=FSInputFile('media/hi.jpg'),
        caption=HELLO_TEXT,
        reply_markup=kb.start_kb()
    )


@router.callback_query(MainPage.filter())
async def comeback(
        call: types.CallbackQuery
):
    try:
        media = types.InputMediaPhoto(media=FSInputFile('media/hi.jpg'), caption=HELLO_TEXT)
        await call.message.edit_media(media=media, reply_markup=kb.start_kb())
    except Exception:
        await call.answer_photo(
            photo=FSInputFile('media/hi.jpg'),
            caption=HELLO_TEXT,
            reply_markup=kb.start_kb()
        )
    await call.answer()
