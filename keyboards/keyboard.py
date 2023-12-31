from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
import datetime as dt
from random import randint
from callbacks import *


class Keyboard:
    def __init__(self):
        pass

    def start_kb(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='Админ', callback_data=UserRole(is_admin=1))
        builder.button(text='Дима',callback_data=UserRole(is_admin=0))
        return builder.as_markup()


    def dimas_kb(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='Актуальная бд товаров', callback_data=DimasFunc(operation=1))
        builder.button(text='Архивы фото',callback_data=DimasFunc(operation=2))
        return builder.as_markup()
