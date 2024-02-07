from aiogram import Router, F, types
from texts import PROFILE_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
from handlers import story_page

router = Router()

def get_bold(text):
    nt = text
    nt = nt.replace('напиток', 'напиток<b>', 1)
    nt = nt.replace('Категория', '</b>Категория', 1)
    nt = nt.replace('Сахар -', 'Сахар -<b>', 1)
    nt = nt.replace('Чиззо-шапка', '</b>Чиззо-шапка<b>', 1)
    nt = nt.replace('Альтернативное молоко - ', '</b>Альтернативное молоко - ', 1)
    nt = nt.replace('Дополнительно:', 'Дополнительно:<b>', 1)
    nt = nt + '</b>'
    if 'Количество' in nt:
        cnt = int(nt[nt.find('Количество'):].split()[1])
    else:
        cnt = 1
    cost = int(nt[nt.find('Итоговая стоимость -'):].split()[3])
    return cost, cnt, nt


@router.callback_query(Count_drink.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery,
        callback_data: Count_drink

):
    if callback_data.name == 'back':
        await call.message.edit_caption(caption=get_bold(call.message.caption)[2],
                                        reply_markup=kb.preadded_kb(callback_data.drink_id))
    elif callback_data.name == 'redo':
        capt = get_bold(call.message.caption)[2]
        if 'Количество' not in call.message.caption:
            capt = '\n'.join(capt.split('\n')[:-1]) + '\nКоличество: <b>1</b>\n' + '\n'.join(capt.split('\n')[-1:])

        await call.message.edit_caption(caption=capt,
                                        reply_markup=kb.redo_count(callback_data.drink_id))
    elif callback_data.name == 'add':
        cost,cnt, capt = get_bold(call.message.caption)
        capt = capt.replace(f'Количество: {cnt}',f'Количество: {cnt+1}',1)
        c = cost//cnt
        capt = capt.replace(f'{cost}',f'{cost+c}',1)
        await call.message.edit_caption(caption=capt, reply_markup=call.message.reply_markup)
    elif callback_data.name == 'minus':
        cost, cnt, capt = get_bold(call.message.caption)
        if cnt == 1:
            await call.answer('Если вы хотите удалить напиток, то просто вернитесь к меню')
        else:
            c = cost // cnt
            capt = capt.replace(f'Количество: {cnt}', f'Количество: {cnt - 1}', 1)
            capt = capt.replace(f'{cost}', f'{cost - c}', 1)
            await call.message.edit_caption(caption=capt, reply_markup=call.message.reply_markup)
    await call.answer()
