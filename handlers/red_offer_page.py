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


def get_bold(text, cost, cnt):
    nt = text
    nt = nt.replace('напиток', 'напиток<b>', 1)
    nt = nt.replace('Категория', '</b>Категория<b>', 1)
    nt = nt.replace('</b>Сахар -', 'Сахар -<b>', 1)
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
    name = kb.db.execute(f"SELECT photo FROM menu WHERE id='{callback_data.offer_id}'").fetchone()[0]
    text = get_bold(*kb.db.execute(
        f"SELECT crit,cost,cnt FROM basket WHERE id='{callback_data.offer_id}' AND chat_id='{call.from_user.id}'").fetchone())
    media = types.InputMediaPhoto(media=FSInputFile(f'media/drinks/{name}'),
                                  caption=text)
    await call.message.edit_media(media=media, reply_markup=kb.back_to_busket(chat_id=call.from_user.id, back=callback_data.back,
                                                                   drink_id=callback_data.drink_id))
    await call.answer()
