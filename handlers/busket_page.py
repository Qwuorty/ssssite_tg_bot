from aiogram import Router, F, types
from texts import PROFILE_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
from handlers import story_page
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, input_file
import random
import os

router = Router()


def number_to_emoji(number):
    emoji_dict = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣'
    }

    result = ''
    for digit in str(number):
        if digit in emoji_dict:
            result += emoji_dict[digit]

    return result


def get_busket_text(chat_id):
    text = 'Вы добавили в корзину:\n\n'
    cnt = 0
    num = 1
    print(len(kb.db.execute(f"SELECT * FROM basket WHERE chat_id='{chat_id}'").fetchall()))
    for info in kb.db.execute(f"SELECT * FROM basket WHERE chat_id='{chat_id}'").fetchall():
        name = kb.db.execute(f"SELECT name FROM menu WHERE id='{info[1]}'").fetchone()[0]
        text += f"   {number_to_emoji(num)} {name} - <b>{int(info[-1]) * int(info[-2])} ₽</b>\n"
        num += 1
        cnt += int(info[-1]) * int(info[-2])
    text += f'\n\nИтого: <b>{cnt} ₽</b>'
    return text


def get_media(text):
    files = os.listdir('media/menu_photo')
    random_file = random.choice(files)
    print(random_file)
    if '.jpg' in random_file:
        media = types.InputMediaPhoto(media=FSInputFile('media/menu_photo/' + random_file),
                                      caption=text)
    else:
        media = types.InputMediaVideo(media=FSInputFile('media/menu_photo/' + random_file),
                                      caption=text)
    return media


@router.callback_query(Busket.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery,
        callback_data: Busket

):
    text = get_busket_text(call.from_user.id)
    if callback_data.back == 'menu':
        await call.message.edit_media(media=get_media(text), reply_markup=kb.busket('menu', chat_id=call.from_user.id))
    elif callback_data.back == 'categorie':
        await call.message.edit_media(media=get_media(text), reply_markup=kb.busket('categorie', callback_data.drink_id,
                                                                                    chat_id=call.from_user.id))
    elif callback_data.back == 'profile':
        await call.message.edit_media(media=get_media(text),
                                      reply_markup=kb.busket('profile', chat_id=call.from_user.id))
    elif callback_data.back == 'drink':
        await call.message.edit_media(media=get_media(text),
                                      reply_markup=kb.busket('drink', int(callback_data.drink_id), call.from_user.id))
    elif callback_data.back == 'add':
        caption = call.message.caption
        crit = caption.split('\n\n\n')[0]
        crit = crit.split('Итоговая стоимость')[0].rstrip()
        cnt = 1 if 'Количество' not in caption else int(caption[caption.find('Количество:'):].split()[1])
        cost = int(caption[caption.find('Итоговая стоимость'):].split()[3]) // cnt
        if kb.sql.execute(
                f"SELECT * FROM basket WHERE crit='{crit}' AND chat_id='{call.from_user.id}' AND tov_id='{callback_data.drink_id}'").fetchone():
            kb.sql.execute(
                f"UPDATE 'basket' SET cnt = cnt+{cnt} WHERE crit='{crit}' AND chat_id='{call.from_user.id}' AND tov_id='{callback_data.drink_id}'")
        else:
            kb.sql.execute("INSERT INTO 'basket' ('chat_id','tov_id','crit','cnt','cost') VALUES (?,?,?,?,?)", (
                call.from_user.id, callback_data.drink_id, crit, cnt, cost))
        kb.db.commit()
        text = get_busket_text(call.from_user.id)
        await call.message.edit_media(media=get_media(text),
                                      reply_markup=kb.busket('drink', int(callback_data.drink_id), call.from_user.id))
    await call.answer()


@router.message(Command("busket"))
async def cmd_start(message: Message):
    text = get_busket_text(message.from_user.id)
    files = os.listdir('media/menu_photo')
    random_file = random.choice(files)
    if '.jpg' in random_file:
        await message.answer_photo(photo=types.FSInputFile('media/menu_photo/' + random_file), caption=text,
                                   reply_markup=kb.busket('menu', chat_id=message.from_user.id))
    else:
        await message.answer_video(video=types.FSInputFile('media/menu_photo/' + random_file), caption=text,
                                   reply_markup=kb.busket('menu', chat_id=message.from_user.id))
