from aiogram import Router
from texts import MENU_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, input_file


router = Router()


@router.callback_query(Menu.filter())
async def menu_page(
        call: types.CallbackQuery
):
    try:
        media = types.InputMediaPhoto(media=FSInputFile('media/main_menu.jpeg'), caption=MENU_TEXT)
        await call.message.edit_media(media=media, reply_markup=kb.menu())
    except Exception as ex:
        await call.message.answer_photo(photo=FSInputFile('media/main_menu.jpeg'),
                                        caption=MENU_TEXT,
                                        reply_markup=kb.menu())
    await call.answer()

@router.message(Command("menu"))
async def cmd_start(message: Message):
    await message.answer_photo(photo=FSInputFile('media/main_menu.jpeg'),
                                        caption=MENU_TEXT,
                                        reply_markup=kb.menu())