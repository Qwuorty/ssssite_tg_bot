from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime as dt
from random import randint
from callbacks import *
import sqlite3


class Keyboard:
    def __init__(self):
        self.db = sqlite3.connect('db.db', check_same_thread=False)
        self.sql = self.db.cursor()

    def number_to_emoji(self, number):
        emoji_dict = {
            '0': '0️⃣',
            '1': '1️⃣',
            '2': '2️⃣',
            '3': '3️⃣',
            '4': '4️⃣',
            '5': '5️⃣',
            '6': '6️⃣',
            '7': '7️⃣',
            '8': '8️⃣',
            '9': '9️⃣'
        }

        result = ''
        for digit in str(number):
            if digit in emoji_dict:
                result += emoji_dict[digit]

        return result

    def contact_kb(self):
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text="Запросить геолокацию", request_location=True),
            types.KeyboardButton(text="Запросить контакт", request_contact=True, request_location=True))
        return builder.as_markup(resize_keyboard=True)

    def start_kb(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='Личный кабинет', callback_data=Profile(back='main'))
        builder.button(text='Сделать заказ', callback_data=Menu())
        return builder.as_markup()

    def back(self, data):
        if data.back == 'main':
            return MainPage()

    def profile(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='История заказов', callback_data=StoryOffers())
        builder.button(text='Контактные данные', callback_data=Contacts())
        builder.button(text='Сделать заказ', callback_data=Menu())
        builder.button(text='Перейти в корзину', callback_data=Busket(back='profile', drink_id='-1'))
        builder.adjust(1)
        return builder.as_markup()

    def busket(self, back, drink_id=None, chat_id=None):
        builder = InlineKeyboardBuilder()
        arr = self.sql.execute(f"SELECT tov_id,cnt,cost,id FROM basket WHERE chat_id='{chat_id}'").fetchall()
        num = 0
        for i in arr:
            num += 1
            builder.button(text=f"{self.number_to_emoji(num)}",
                           callback_data=RedOffer(drink_id=str(i[0]), offer_id=int(i[3]), back=back))
        if back == 'drink':
            builder.button(text='Назад', callback_data=Drink(drink_id=drink_id))
        elif back == 'profile':
            builder.button(text='Назад', callback_data=Profile(back='-1'))
        elif back == 'categorie':
            builder.button(text='Назад', callback_data=Categories(name=drink_id))
        elif back == 'menu':
            builder.button(text='Назад', callback_data=Menu())
        builder.button(text='Оплатить', callback_data=Profile(back='add'))
        sz = []
        while num != 0:
            sz.append(4 if num % 4 == 0 else num % 4)
            num //= 4
        sz.append(1)
        print(sz)
        builder.adjust(*sz)
        return builder.as_markup()

    def back_to_busket(self, back, drink_id=None, chat_id=None, offer_id=None):
        builder = InlineKeyboardBuilder()
        cnt = kb.db.execute(f"SELECT cnt FROM basket WHERE id='{offer_id}'").fetchone()[0]
        offer_id = str(offer_id)
        if cnt == 1:
            builder.button(text=f'Удалить',
                           callback_data=AddBusket(name='shure_delete', drink_id=drink_id, back=back,
                                                   offer_id=offer_id))
            builder.button(text=f'➕',
                           callback_data=AddBusket(name='add', drink_id=drink_id, back=back, offer_id=offer_id))
        else:
            builder.button(text=f'➖',
                           callback_data=AddBusket(name='minus', drink_id=drink_id, back=back, offer_id=offer_id))
            builder.button(text=f'➕',
                           callback_data=AddBusket(name='add', drink_id=drink_id, back=back, offer_id=offer_id))
        builder.button(text='Назад', callback_data=Busket(back=back, drink_id=str(drink_id)))
        builder.adjust(2, 1)
        return builder.as_markup()

    def story(self, name='story'):
        builder = InlineKeyboardBuilder()
        builder.button(text='Личный кабинет', callback_data=Profile(back=name))
        builder.adjust(1)
        return builder.as_markup()

    def contact(self):
        return self.story(name='contact')

    def menu(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='Боба', callback_data=Categories(name='Боба'))
        builder.button(text='Йогурт', callback_data=Categories(name='Йогурт'))
        builder.button(text='Чиззо', callback_data=Categories(name='Чиззо'))
        builder.button(text='Лактис', callback_data=Categories(name='Лактис'))
        builder.button(text='Кофе', callback_data=Categories(name='Кофе'))
        builder.button(text='Фруктовый', callback_data=Categories(name='Фруктовый'))
        builder.button(text='Простой чай', callback_data=Categories(name='Простой чай'))
        builder.button(text='Личный кабинет', callback_data=Profile(back='menu'))
        builder.button(text='Перейти в корзину', callback_data=Busket(back='menu', drink_id='-1'))
        builder.adjust(2, 2, 2, 1, 1, 1)
        return builder.as_markup()

    def categories(self, name):
        builder = InlineKeyboardBuilder()
        size = len(self.sql.execute(f"SELECT name FROM menu WHERE type='{name}'").fetchall())
        for drink in self.sql.execute(f"SELECT * FROM menu WHERE type='{name}'").fetchall():
            builder.button(text=drink[1], callback_data=Drink(drink_id=int(drink[0])))
        builder.button(text=f'Назад в меню', callback_data=Menu())
        builder.button(text='Перейти в корзину', callback_data=Busket(back='categorie', drink_id=str(name)))
        arr = [2 for _ in range(size // 2)]
        arr.append(1)
        arr.append(1)
        builder.adjust(*arr)
        return builder.as_markup()

    def admin_kb(self):
        builder = InlineKeyboardBuilder()
        builder.button(text=f'Статистика', callback_data=Admin(oper='stat'))
        builder.button(text=f'История', callback_data=Admin(oper='story_zak'))
        builder.button(text=f'Заказы', callback_data=Admin(oper='zakaz'))
        builder.button(text=f'СтопЛист', callback_data=Admin(oper='stops'))
        builder.adjust(1)
        return builder.as_markup()

    def get_stops(self, point_id):
        builder = InlineKeyboardBuilder()
        arr = self.sql.execute(f"SELECT tov_id FROM stop WHERE point='{point_id}'").fetchall()
        for i in self.sql.execute(f"SELECT id FROM menu").fetchall():
            name, cat = self.sql.execute(f"SELECT name, type FROM menu WHERE id='{i[0]}'").fetchone()
            if i in arr:
                builder.button(text='❌'+name + ' ' + cat, callback_data=RedStop(point_id=int(point_id), tov_id=int(i[0])))
            else:
                builder.button(text='✅'+name + ' ' + cat, callback_data=RedStop(point_id=int(point_id), tov_id=int(i[0])))
        builder.button(text=f'Назад', callback_data=Admin(oper='back'))
        builder.adjust(1)
        return builder.as_markup()

    def redo_count(self, drink_id):
        builder = InlineKeyboardBuilder()
        builder.button(text=f'➕', callback_data=Count_drink(name='add', drink_id=drink_id))
        builder.button(text=f'➖', callback_data=Count_drink(name='minus', drink_id=drink_id))
        builder.button(text=f'Назад', callback_data=Count_drink(name='back', drink_id=drink_id))

        builder.adjust(2, 1)
        return builder.as_markup()

    def preadded_kb(self, drink_id):
        builder = InlineKeyboardBuilder()
        builder.button(text=f'Назад', callback_data=Drink(drink_id=drink_id))
        builder.button(text=f'Изменить количество', callback_data=Count_drink(drink_id=drink_id, name='redo'))
        builder.button(text=f'Добавить в корзину', callback_data=Busket(drink_id=str(drink_id), back='add'))
        builder.adjust(1)
        return builder.as_markup()

    def shure_delete(self, back, drink_id, offer_id, name):
        builder = InlineKeyboardBuilder()
        builder.button(text='Да, удалить',
                       callback_data=AddBusket(drink_id=drink_id, name='delete', offer_id=offer_id, back=back))
        builder.button(text='Нет', callback_data=RedOffer(drink_id=drink_id, back=back, offer_id=offer_id))
        builder.adjust(2)
        return builder.as_markup()

    def open_dops(self, drink_id, kb):
        builder = InlineKeyboardBuilder()
        sizes = []
        dops = (self.sql.execute(f"SELECT dops FROM menu WHERE id='{drink_id}'").fetchone()[0]).split(';')[1:]

        def add_dops_buttons():
            for dop in dops[0].split(':')[1].split(','):
                dop_name = dop[1:-1]
                if 'сахар' in dop_name:
                    builder.button(text=dop_name + '₽',
                                   callback_data=Options(option_name=dop_name, type_name='sugar',
                                                         drink_id=drink_id))
                elif 'чиззо-шапк' in dop_name.lower():
                    builder.button(text=dop_name + '₽',
                                   callback_data=Options(option_name=dop_name, type_name='chisso_hat',
                                                         drink_id=drink_id))
                else:
                    builder.button(text=dop_name + '₽',
                                   callback_data=Options(option_name=dop_name, type_name='default_dop',
                                                         drink_id=drink_id))

        for i in kb.inline_keyboard:
            sizes.append(len(i))
            for j in i:
                if j.text == '🔽 Дополнительно 🔽':
                    builder.button(text='🔼 Дополнительно 🔼',
                                   callback_data=Options(option_name='opened', type_name='redo_dops',
                                                         drink_id=drink_id))
                    add_dops_buttons()
                    for _ in range(len(dops[0].split(':')[1].split(',')) // 2):
                        sizes.append(2)
                    if len(dops[0].split(':')[1].split(',')) % 2:
                        sizes.append(1)
                    if len(dops) == 2:
                        # если есть возможность смены молока - добавляем кнопку
                        builder.button(text='🔽 Альтернативное молоко 🔽',
                                       callback_data=Options(option_name='closed', type_name='redo_milk',
                                                             drink_id=drink_id))
                        sizes.append(1)
                else:
                    builder.button(text=j.text, callback_data=j.callback_data)
        builder.adjust(*sizes)
        return builder.as_markup()

    def open_milk(self, drink_id, kb):
        builder = InlineKeyboardBuilder()
        sizes = []
        milk = (self.sql.execute(f"SELECT dops FROM menu WHERE id='{drink_id}'").fetchone()[0]).split(';')[2:]

        def add_dops_buttons():
            # добавляем кнопки к клавиатуре с допольнительными опциями
            for dop in milk[0].split(':')[1].split(','):
                dop_name = dop[1:-1]
                builder.button(text=dop_name + '₽',
                               callback_data=Options(option_name=dop_name, type_name='alt_milk',
                                                     drink_id=drink_id))

        for i in kb.inline_keyboard:
            sizes.append(len(i))
            for j in i:
                if j.text == '🔽 Альтернативное молоко 🔽':
                    builder.button(text='🔼 Альтернативное молоко 🔼',
                                   callback_data=Options(option_name='opened', type_name='redo_milk',
                                                         drink_id=drink_id))
                    add_dops_buttons()
                    for _ in range(len(milk[0].split(':')[1].split(',')) // 2):
                        sizes.append(2)
                    if len(milk[0].split(':')[1].split(',')) % 2:
                        sizes.append(1)
                else:
                    builder.button(text=j.text, callback_data=j.callback_data)
        builder.adjust(*sizes)
        return builder.as_markup()

    def close_milk(self, drink_id, kb):
        builder = InlineKeyboardBuilder()
        sizes = []
        flag = 1
        for i in kb.inline_keyboard:
            if flag:
                sizes.append(len(i))
            for j in i:
                if j.text == '🔼 Альтернативное молоко 🔼':
                    flag = 0
                    builder.button(text='🔽 Альтернативное молоко 🔽',
                                   callback_data=Options(option_name='closed', type_name='redo_milk',
                                                         drink_id=drink_id))
                elif flag or '+' not in j.text:
                    builder.button(text=j.text, callback_data=j.callback_data)
        if self.sql.execute(f"SELECT type FROM menu WHERE id='{drink_id + 1}'").fetchone()[0].split(';')[0] == \
                self.sql.execute(f"SELECT type FROM menu WHERE id='{drink_id}'").fetchone()[0].split(';')[0]:
            sizes = [*sizes, 2, 2]
        else:
            sizes = [*sizes, 2, 2]

        builder.adjust(*sizes)
        return builder.as_markup()

    def close_dops(self, drink_id, kb):
        builder = InlineKeyboardBuilder()
        sizes = []
        flag = 1
        for i in kb.inline_keyboard:
            if flag:
                sizes.append(len(i))
            for j in i:
                if j.text == '🔼 Дополнительно 🔼':
                    flag = 0
                    builder.button(text='🔽 Дополнительно 🔽',
                                   callback_data=Options(option_name='closed', type_name='redo_dops',
                                                         drink_id=drink_id))
                elif ('+' not in j.text or 'мл' in j.text) and 'Альтернативное молоко' not in j.text:
                    sizes.append(1)
                    builder.button(text=j.text, callback_data=j.callback_data)
        if self.sql.execute(f"SELECT type FROM menu WHERE id='{drink_id + 1}'").fetchone()[0].split(';')[0] == \
                self.sql.execute(f"SELECT type FROM menu WHERE id='{drink_id}'").fetchone()[0].split(';')[0]:
            sizes = [sizes[0], 1, 2, 2]
        else:
            sizes = [sizes[0], 1, 1, 2]

        builder.adjust(*sizes)
        return builder.as_markup()

    def drink_kb(self, drink_id):
        print(drink_id)
        builder = InlineKeyboardBuilder()
        dops = (
            self.sql.execute(f"SELECT dops FROM menu WHERE id='{drink_id}'").fetchone()[0]).split(';')
        drink_type = (
            self.sql.execute(f"SELECT type FROM menu WHERE id='{drink_id}'").fetchone()[0]).split(';')[0]
        volume = dops[0].split(':')[1].split(',')
        for volume_type in volume:
            builder.button(text=volume_type[1:-1] + '₽',
                           callback_data=Options(option_name=volume_type,
                                                 type_name='volume',
                                                 drink_id=drink_id)
                           )
        builder.button(text='🔽 Дополнительно 🔽',
                       callback_data=Options(option_name='closed',
                                             type_name='redo_dops',
                                             drink_id=drink_id)
                       )
        builder.button(text=f'Назад',
                       callback_data=Categories(name=drink_type)
                       )
        next_type = self.sql.execute(f"SELECT type FROM menu WHERE id='{drink_id + 1}'").fetchone()
        if next_type:
            next_type = next_type[0].split(';')[0]
        step = 1
        if next_type == drink_type:
            builder.button(text=f' → ',
                           callback_data=Drink(drink_id=drink_id + 1)
                           )
            step = 2
        builder.button(text='Перейти в корзину',
                       callback_data=Busket(back='drink', drink_id=str(drink_id))
                       )
        builder.button(text='Добавить в корзину',
                       callback_data=AddDrink(back='drink', drink_id=str(drink_id))
                       )
        builder.adjust(dops[0].count('мл'), 1, step, 2)
        return builder.as_markup()


kb = Keyboard()
