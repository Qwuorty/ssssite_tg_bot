from aiogram import Router, F, types
from texts import PROFILE_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
from handlers import story_page
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, input_file
import os, random

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


def get_bold(text, cost, cnt):
    nt = text
    nt = nt.replace('напиток', 'напиток<b>', 1)
    nt = nt.replace('Категория', '</b>Категория<b>', 1)
    nt = nt.replace('</b>Сахар -', 'Сахар -<b>', 1)
    nt = nt.replace('Объём -', '</b>Объём -<b>', 1)
    nt = nt.replace('Чиззо-шапка', '</b>Чиззо-шапка<b>', 1)
    nt = nt.replace('Альтернативное молоко - ', '</b>Альтернативное молоко - <b>', 1)
    nt = nt.replace('</b>Дополнительно:', 'Дополнительно:<b>', 1)
    nt = nt + '</b>'
    nt += f'''

<b>Количество: {cnt}</b>
<b>Итоговая стоимость: {int(cnt) * int(cost)} ₽</b>'''
    return nt


@router.callback_query(RedOffer.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery,
        callback_data: RedOffer):
    drin_id = kb.db.execute(f"SELECT tov_id FROM basket WHERE id='{callback_data.offer_id}'").fetchone()[0]
    name = kb.db.execute(f"SELECT photo FROM menu WHERE id='{drin_id}'").fetchone()[0]
    text = get_bold(*kb.db.execute(
        f"SELECT crit,cost,cnt FROM basket WHERE id='{callback_data.offer_id}' AND chat_id='{call.from_user.id}'").fetchone())
    media = types.InputMediaPhoto(media=FSInputFile(f'media/drinks/{name}'),
                                  caption=text)
    await call.message.edit_media(media=media,
                                  reply_markup=kb.back_to_busket(chat_id=call.from_user.id, back=callback_data.back,
                                                                 drink_id=callback_data.drink_id,
                                                                 offer_id=callback_data.offer_id))
    await call.answer()


@router.callback_query(AddBusket.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery,
        callback_data: AddBusket):
    if callback_data.name == 'add':
        kb.db.execute(f"UPDATE basket SET cnt= cnt+1 WHERE id='{callback_data.offer_id}'")
        kb.db.commit()
        text = get_bold(*kb.db.execute(
            f"SELECT crit,cost,cnt FROM basket WHERE id='{callback_data.offer_id}' AND chat_id='{call.from_user.id}'").fetchone())
        await call.message.edit_caption(caption=text,
                                        reply_markup=kb.back_to_busket(chat_id=call.from_user.id,
                                                                       back=callback_data.back,
                                                                       drink_id=callback_data.drink_id,
                                                                       offer_id=callback_data.offer_id))

    elif callback_data.name == 'minus':
        kb.db.execute(f"UPDATE basket SET cnt= cnt-1 WHERE id='{callback_data.offer_id}'")
        kb.db.commit()
        text = get_bold(*kb.db.execute(
            f"SELECT crit,cost,cnt FROM basket WHERE id='{callback_data.offer_id}' AND chat_id='{call.from_user.id}'").fetchone())
        await call.message.edit_caption(caption=text,
                                        reply_markup=kb.back_to_busket(chat_id=call.from_user.id,
                                                                       back=callback_data.back,
                                                                       drink_id=callback_data.drink_id,
                                                                       offer_id=callback_data.offer_id))

    elif callback_data.name == 'shure_delete':
        print(callback_data)
        await call.message.edit_reply_markup(
            reply_markup=kb.shure_delete(callback_data.back, callback_data.drink_id, callback_data.offer_id,
                                         callback_data.name))
    elif callback_data.name == 'delete':
        kb.db.execute(f"DELETE FROM basket WHERE id='{callback_data.offer_id}'")
        kb.db.commit()
        text = get_busket_text(call.from_user.id)
        if callback_data.back == 'menu':
            await call.message.edit_media(media=get_media(text),
                                          reply_markup=kb.busket('menu', chat_id=call.from_user.id))
        elif callback_data.back == 'categorie':
            await call.message.edit_media(media=get_media(text),
                                          reply_markup=kb.busket('categorie', callback_data.drink_id,
                                                                 chat_id=call.from_user.id))
        elif callback_data.back == 'profile':
            await call.message.edit_media(media=get_media(text),
                                          reply_markup=kb.busket('profile', chat_id=call.from_user.id))
        elif callback_data.back == 'drink':
            await call.message.edit_media(media=get_media(text),
                                          reply_markup=kb.busket('drink', int(callback_data.drink_id),
                                                                 call.from_user.id))
        await call.answer()
