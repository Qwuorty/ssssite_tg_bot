from aiogram import Router, F, types
from texts import PROFILE_TEXT, CATEGORIES_TEXT,points
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb
from handlers import red_offer_page

router = Router()


@router.callback_query(RedStop.filter())
async def drink(
        call: types.CallbackQuery,
        callback_data: RedStop
):
    if kb.sql.execute(
            f"SELECT * FROM stop WHERE point='{callback_data.point_id}' AND tov_id='{callback_data.tov_id}'").fetchone():
        kb.sql.execute(f"DELETE FROM stop WHERE point='{callback_data.point_id}' AND tov_id='{callback_data.tov_id}'")
        kb.db.commit()
    else:
        kb.sql.execute(f"INSERT INTO stop (point,tov_id) VALUES ({callback_data.point_id},{callback_data.tov_id})")
        kb.db.commit()
    await call.message.edit_text(text=f'Стоп лист для точки по адресу {points[callback_data.point_id]}',
                                 reply_markup=kb.get_stops(callback_data.point_id))
    await call.answer()
