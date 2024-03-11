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
        call: types.CallbackQuery,
        callback_data: Profile
):
    if callback_data.back == 'add':
        for i in kb.sql.execute(f"SELECT * FROM basket WHERE chat_id='{call.from_user.id}'").fetchall():
            text = i[2]
            drink_id = i[1]
            name, cat = kb.sql.execute(f"SELECT name,type FROM menu WHERE id='{drink_id}'").fetchone()
            sugar = ' '.join(text[text.find('Сахар - '):text.find('\n\nЧиззо-шапка')].split()[2:]).split('+')[0]
            chisso = (text[text.find('Чиззо-шапка'):text.find('\n\nАльтернативное молоко')]).split('+')[0]
            milk =  text[text.find('Альтернативное молоко -')+24:]
            milk = milk[:milk.find('\n\n')].split('+')[0]
            dops = text[text.find('Дополнительно:')+15:].split('\n')
            for j in range(len(dops)):
                dops[j] = dops[j].split('+')[0]
            '\n'.join(dops)
    else:
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
