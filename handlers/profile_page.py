from aiogram import Router, F, types, Bot
from texts import PROFILE_TEXT, point_admins,bot2
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
import datetime as dt
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
        all_info = []
        for i in kb.sql.execute(f"SELECT * FROM basket WHERE chat_id='{call.from_user.id}'").fetchall():
            text = i[2]
            drink_id = i[1]
            cnt = int(i[4])
            cost_for_one = int(i[5])
            name, cat = kb.sql.execute(f"SELECT name,type FROM menu WHERE id='{drink_id}'").fetchone()
            sugar = ' '.join(text[text.find('Сахар - '):text.find('\n\nЧиззо-шапка')].split()[2:]).split('+')[0]
            chisso = (text[text.find('Чиззо-шапка'):text.find('\n\nАльтернативное молоко')]).split('+')[0]
            milk = text[text.find('Альтернативное молоко -') + 24:]
            milk = milk[:milk.find('\n\n')].split('+')[0]
            dops = text[text.find('Дополнительно:') + 15:].split('\n')
            new_dops = []
            for j in range(len(dops)):
                if 'Количество' not in dops[j]:
                    new_dops.append(dops[j].split('+')[0])
            dops = new_dops
            '\n'.join(dops)
            value = text[text.find('Объём -') + 7:]
            value = value.split('+')[0].strip()
            info = f"""
Напиток - {name}
Категория - {cat}
Объем - {value}
Сахар - {sugar}
{chisso}
Молоко - {milk}
Допы - {'\n'.join(dops)}
Количество - {cnt}"""
            all_info.append(info)
        add_info = '\n\n\n'.join(all_info)
        point_id = 1
        dt_now = str(dt.datetime.now())
        kb.sql.execute(f"INSERT INTO orders (dt,chat_id,status,info,point_id) VALUES ('{dt_now}'"
                       f",'{call.from_user.id}','wait','{add_info}','{point_id}')")
        kb.sql.execute(f"DELETE FROM basket WHERE chat_id='{call.from_user.id}'")
        kb.db.commit()
        for i in point_admins[point_id]:
            await bot2.send_message(chat_id=i, text='Внимание, новый заказ\n' + add_info)
        await call.message.answer('Мы уже приняли ваш заказ и начали его готовить')
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
