from aiogram import Router
from texts import PROFILE_TEXT, CATEGORIES_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
from handlers import story_page

router = Router()


@router.callback_query(AddDrink.filter())
async def pre_added_check_of_add(
        call: types.CallbackQuery,
        callback_data: AddDrink
):
    drink_name = kb.sql.execute(f"SELECT name FROM menu WHERE id='{callback_data.drink_id}'").fetchone()[0]
    caregorie_name = kb.sql.execute(f"SELECT type FROM menu WHERE id='{callback_data.drink_id}'").fetchone()[0]
    sugar = 'Стандартный'
    chisso = 'Стандартная'
    alt_milk = 'Не выбрано'
    price = int(call.message.caption.split('\n')[-1].split()[0])
    dops = []
    for row in call.message.reply_markup.inline_keyboard:
        for button in row:
            if '✅' in button.text:
                if 'sugar' in button.callback_data:
                    sugar = button.text.split('✅')[1].strip()
                elif 'chisso_hat' in button.callback_data:
                    chisso = button.text.split('✅')[1].strip()
                elif 'default_dop' in button.callback_data:
                    dops.append(button.text.split('✅')[1].strip())
                elif 'alt_milk' in button.callback_data:
                    alt_milk = (button.text.split('✅')[1].strip())
    dops_text = ''.join(["<b>•\t" + i + '</b>\n' for i in dops])
    if dops_text == '':
        dops_text='<b> Не выбранно</b>'
    capti = f'''Вы выбрали напиток <b>{drink_name}</b>
Категория - <b>{caregorie_name}</b>

Сахар - <b>{sugar}</b>

Чиззо-шапка - <b>{chisso}</b>

Альтернативное молоко - <b>{alt_milk}</b>

Дополнительно: \n{dops_text}

Итоговая стоимость - <b>{price} ₽</b>'''
    await call.message.edit_caption(caption=capti, reply_markup=kb.preadded_kb(callback_data.drink_id))
    await call.answer()
