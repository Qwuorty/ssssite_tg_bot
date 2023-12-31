from aiogram import Router, F,types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards import keyboard
from handlers import dimas_page
from callbacks import *


router = Router()  # [2]
kb = keyboard.Keyboard()
router.include_routers(dimas_page.router2)


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    await message.answer(
        "Кто вы?",
        reply_markup=kb.start_kb()
    )


@router.callback_query(UserRole.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery,
        callback_data: UserRole
):
    data = callback_data
    try:
        if data.is_admin:
            await call.message.edit_text("ты админ")
        else:
            await call.message.edit_text("привет, Дима",reply_markup=kb.dimas_kb())
    except:
        if data.is_admin:
            await call.message.answer("ты админ")
        else:
            await call.message.answer("привет, Дима",reply_markup=kb.dimas_kb())
    await call.answer()

