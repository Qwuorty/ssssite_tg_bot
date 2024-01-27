from aiogram import Router, F, types
from texts import PROFILE_TEXT, CATEGORIES_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb

router = Router()


@router.callback_query(Options.filter())
async def update_options_kb(
        call: types.CallbackQuery,
        callback_data: Options
):
    if callback_data.type_name == 'volume':
        repl = call.message.reply_markup
        row = repl.inline_keyboard[0]
        for j in row:
            if j.callback_data == call.data:
                if '✅' in j.text:
                    await call.answer('Вы уже выбрали этот объём')
                    return
        delta = 0
        for j in range(len(row)):
            if '✅' in row[j].text and row[j].text != '✅':
                row[j].text = row[j].text[2:]
                delta -= int(row[j].text.split('+')[1])
            else:
                row[j].text = '✅ ' + row[j].text
                delta += int(row[j].text.split('+')[1])
        new_caption = call.message.caption
        price = int(new_caption.split('\n')[-1].split()[0])
        new_caption = ''.join(new_caption.split('\n')[:-1])+'\n'+f'<b>{price+delta}</b> ₽'
        await call.message.edit_caption(caption=new_caption, reply_markup=repl)
    await call.answer()
