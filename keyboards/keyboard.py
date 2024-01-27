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
        for drink in self.sql.execute(f"SELECT name FROM menu WHERE type='{name}'").fetchall():
            builder.button(text=drink[0], callback_data=Drink(name=drink[0], categorie=name))
        builder.button(text=f'Назад в меню', callback_data=Menu())
        builder.button(text='Перейти в корзину', callback_data=Busket(back='menu'))
        arr = [2 for _ in range(size // 2)]
        arr.append(1)
        arr.append(1)
        builder.adjust(*arr)
        return builder.as_markup()

    def drink_kb(self, name, drink_type):
        builder = InlineKeyboardBuilder()
        dops = (
        self.sql.execute(f"SELECT dops FROM menu WHERE type='{drink_type}' AND name='{name}'").fetchone()[0]).split(';')
        volume = dops[0].split(':')[1].split(',')
        for volume_type in volume:
            builder.button(text=volume_type[1:-1], callback_data=Options(option_name=volume_type, type_name='volume'))
        builder.button(text=f'Назад', callback_data=Categories(name=drink_type))
        builder.button(text='Перейти в корзину', callback_data=Busket(back='menu'))
        builder.adjust(2, 1, 1)
        return builder.as_markup()


kb = Keyboard()
