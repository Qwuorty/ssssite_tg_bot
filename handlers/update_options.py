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
    elif callback_data.type_name == 'sugar':
        replace_sugar = None
        new_reply_markup = call.message.reply_markup
        for row in new_reply_markup.inline_keyboard:
            for button in row:
                if callback_data.option_name in button.callback_data:
                    if '✅' in button.text:
                        await call.answer('Вы уже выбрали это количество сахара для вашего напитка')
                        return
                    else:
                        replace_sugar = 1
        if replace_sugar:
            for row in new_reply_markup.inline_keyboard:
                for button in row:
                    if 'sugar' in button.callback_data:
                        if callback_data.option_name in button.callback_data:
                            button.text = '✅ ' + button.text
                        elif '✅' in button.text:
                            button.text = button.text.split('✅')[1].strip()
        await call.message.edit_caption(caption=call.message.caption, reply_markup=new_reply_markup)
    elif callback_data.type_name == 'chisso_hat':
        replace_chisso = None
        new_price = int(call.message.caption.split('\n')[-1].split('₽')[0])
        new_reply_markup = call.message.reply_markup
        for row in new_reply_markup.inline_keyboard:
            for button in row:
                if callback_data.option_name in button.callback_data:
                    if '✅' in button.text:
                        await call.answer('Вы уже выбрали этe опцию Чиззо-шапки')
                        return
                    else:
                        replace_chisso = 1
        if replace_chisso:
            for row in new_reply_markup.inline_keyboard:
                for button in row:
                    if 'chisso_hat' in button.callback_data:
                        if callback_data.option_name in button.callback_data:
                            button.text = '✅ ' + button.text
                            new_price += int(button.text.split('+')[1].split('₽')[0])
                        elif '✅' in button.text:
                            button.text = button.text.split('✅')[1].strip()
                            new_price -= int(button.text.split('+')[1].split('₽')[0])
        new_caption = '\n'.join(call.message.caption.split('\n')[:-1])+'\n'+f"<b>{new_price} ₽</b>"
        await call.message.edit_caption(caption=new_caption, reply_markup=new_reply_markup)

    await call.answer()
