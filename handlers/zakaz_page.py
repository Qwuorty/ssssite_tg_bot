from aiogram import Router, F, types
from texts import PROFILE_TEXT, month_names
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
from handlers import story_page
import datetime as dt
from texts import bot2


router = Router()


@router.callback_query(Offer.filter())
async def callbacks_num_change_fab(
        call: types.CallbackQuery,
        callback_data: Offer

):
    if callback_data.offer_id < 0:
        offer_id = -callback_data.offer_id
        chat_id = kb.sql.execute(f"SELECT chat_id FROM orders WHERE id='{offer_id}'").fetchone()[0]
        kb.sql.execute(f"UPDATE orders SET status='end' WHERE id='{offer_id}'")
        kb.db.commit()
        await bot2.send_message(chat_id, 'Ваш заказ готов!')
    else:
        arr = kb.sql.execute(f"SELECT * FROM orders WHERE id='{callback_data.offer_id}'").fetchone()
        text = arr[4]
        date_obj = dt.datetime.strptime(arr[1], "%Y-%m-%d %H:%M:%S.%f")
        formatted_date = date_obj.strftime("%d %B %H:%M")
        arr_dt = formatted_date.split()
        arr_dt[1] = month_names[arr_dt[1]]
        text = f"Заказ от        {' '.join(arr_dt)}\nНомер телефона - {kb.sql.execute(f"SELECT number FROM users WHERE chat_id='{arr[2]}'").fetchone()[0]}\n" + text
        await call.message.edit_text(text=text, reply_markup=kb.get_offer_kb(callback_data.offer_id))
    await call.answer()
