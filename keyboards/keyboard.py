from aiogram.utils.keyboard import InlineKeyboardBuilder
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
        builder.button(text='Перейти в корзину', callback_data=Busket(back='profile'))
        builder.adjust(1)
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
        builder.button(text='Перейти в корзину', callback_data=Busket(back='menu'))
        builder.adjust(2, 2, 2, 1, 1, 1)
        return builder.as_markup()

    def categories(self, name):
        builder = InlineKeyboardBuilder()
        size = len(self.sql.execute(f"SELECT name FROM menu WHERE type='{name}'").fetchall())
        for drink in self.sql.execute(f"SELECT * FROM menu WHERE type='{name}'").fetchall():
            builder.button(text=drink[1], callback_data=Drink(drink_id=int(drink[0])))
        builder.button(text=f'Назад в меню', callback_data=Menu())
        builder.button(text='Перейти в корзину', callback_data=Busket(back='menu'))
        arr = [2 for _ in range(size // 2)]
        arr.append(1)
        arr.append(1)
        builder.adjust(*arr)
        return builder.as_markup()

    def redo_count(self,drink_id,text):
        builder = InlineKeyboardBuilder()
        builder.button(text=f'Назад', callback_data=Add_drink(back='drink', drink_id=drink_id,text=text))
        builder.adjust(1)
        return builder.as_markup()

    def preadded_kb(self, drink_id):
        builder = InlineKeyboardBuilder()
        builder.button(text=f'Назад', callback_data=Drink(drink_id=drink_id))
        builder.button(text=f'Изменить количество', callback_data=Count_drink(drink_id=drink_id,name='redo'))
        builder.button(text='Перейти в корзину', callback_data=Busket(back='menu'))
        builder.adjust(1)
        return builder.as_markup()

    def open_dops(self, drink_id, kb):
        builder = InlineKeyboardBuilder()
        sizes = []
        dops = (self.sql.execute(f"SELECT dops FROM menu WHERE id='{drink_id}'").fetchone()[0]).split(';')[1:]

        def add_dops_buttons():
            # добавляем кнопки к клавиатуре с допольнительными опциями
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
                elif ('+' not in j.text or 'мл' in j.text) and j.text != '🔽 Альтернативное молоко 🔽':
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
        next_type = self.sql.execute(f"SELECT type FROM menu WHERE id='{drink_id + 1}'").fetchone()[0].split(';')[0]
        step = 1
        if next_type == drink_type:
            builder.button(text=f' → ',
                           callback_data=Drink(drink_id=drink_id + 1)
                           )
            step = 2
        builder.button(text='Перейти в корзину',
                       callback_data=Busket(back='menu')
                       )
        builder.button(text='Добавить в корзину',
                       callback_data=AddDrink(back='drink', drink_id=str(drink_id))
                       )
        builder.adjust(dops[0].count('мл'), 1, step, 2)
        return builder.as_markup()


kb = Keyboard()
