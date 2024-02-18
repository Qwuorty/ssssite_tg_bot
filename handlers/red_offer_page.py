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


@router.callback_query(RedOffer.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery,
        callback_data: RedOffer

):
    await call.message.edit_caption('123',
                                    reply_markup=kb.back_to_busket(chat_id=call.from_user.id, back=callback_data.back,
                                                                   drink_id=callback_data.drink_id))
    await call.answer()
