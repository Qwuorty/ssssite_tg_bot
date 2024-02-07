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


@router.callback_query(Busket.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery,
        callback_data: Busket

):
    if callback_data.back == 'menu':
        print('меню')
        media = types.InputMediaPhoto(media=FSInputFile(f'media/menu_photo.jpg'),
                                      caption='text')
        await call.message.edit_media(media=media, reply_markup=kb.busket('menu', chat_id=call.from_user.id))
    elif callback_data.back == 'categorie':
        print('категория')
        media = types.InputMediaPhoto(media=FSInputFile(f'media/menu_photo.jpg'),
                                      caption='text')
        await call.message.edit_media(media=media, reply_markup=kb.busket('categorie', callback_data.drink_id,
                                                                          chat_id=call.from_user.id))
    elif callback_data.back == 'profile':
        print('профиль')
        media = types.InputMediaPhoto(media=FSInputFile(f'media/menu_photo.jpg'),
                                      caption='text')
        await call.message.edit_media(media=media, reply_markup=kb.busket('profile', chat_id=call.from_user.id))
    elif callback_data.back == 'drink':
        media = types.InputMediaPhoto(media=FSInputFile(f'media/menu_photo.jpg'),
                                      caption='text')
        await call.message.edit_media(media=media,
                                      reply_markup=kb.busket('drink', int(callback_data.drink_id), call.from_user.id))

    elif callback_data.back == 'add':
        caption = call.message.caption
        crit = caption.split('\n\n\n')[0]
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
        await call.answer()


@router.message(Command("busket"))
async def cmd_start(message: Message):
    await message.answer_photo(photo=FSInputFile(f'media/menu_photo.jpg'),
                               caption='text',
                               reply_markup=kb.busket('menu',chat_id=message.from_user.id))
