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
        # обновляем объем для напитка
        repl, row = call.message.reply_markup, call.message.reply_markup.inline_keyboard[0]
        # прекращаем функцию, если нажали на уже выбранную опцию
        for j in row:
            if j.callback_data == call.data:
                if '✅' in j.text:
                    await call.answer('Вы уже выбрали этот объём')
                    return
        price = int(call.message.caption.split('\n')[-1].split()[0])
        for j in range(len(row)):
            if '✅' in row[j].text and row[j].text != '✅':
                row[j].text = row[j].text[2:]
                price -= int(row[j].text.split('+')[1][:-1])
            else:
                row[j].text = '✅ ' + row[j].text
                price += int(row[j].text.split('+')[1][:-1])
        new_caption_with_updated_price = ''.join(call.message.caption.split('\n')[:-1]) + '\n' + f'<b>{price}</b> ₽'
        await call.message.edit_caption(caption=new_caption_with_updated_price, reply_markup=repl)
    elif callback_data.type_name == 'redo_dops':
        if callback_data.option_name == 'closed':
            await call.message.edit_caption(caption=call.message.caption,
                                            reply_markup=kb.open_dops(callback_data.drink_id,
                                                                      call.message.reply_markup)
                                            )
        elif callback_data.option_name == 'opened':
            await call.message.edit_caption(caption=call.message.caption,
                                            reply_markup=kb.close_dops(callback_data.drink_id,
                                                                       call.message.reply_markup)
                                            )

    await call.answer()
