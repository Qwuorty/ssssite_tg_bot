from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime as dt
from random import randint
from callbacks import *


class Keyboard:
    def __init__(self):
        pass

    def start_kb(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='Личный кабинет', callback_data=Profile(back='main'))
        builder.button(text='Сделать заказ', callback_data=MakeOffer(back='main'))
        return builder.as_markup()

    def back(self, data):
        if data.back == 'main':
            return MainPage()

    def profile(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='История заказов', callback_data=StoryOffers())
        builder.button(text='Контактные данные', callback_data=Contacts())
        builder.button(text='Моя корзина', callback_data=Busket(back='profile'))
        builder.button(text='Меню', callback_data=Menu())
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
        builder.button(text='Боба', callback_data=Categorie(name='Боба'))
        builder.button(text='Йогурт', callback_data=Categorie(name='Йогурт'))
        builder.button(text='Чиззо', callback_data=Categorie(name='Чиззо'))
        builder.button(text='Лактис', callback_data=Categorie(name='Лактис'))
        builder.button(text='Кофе', callback_data=Categorie(name='Кофе'))
        builder.button(text='Фруктовый', callback_data=Categorie(name='Фруктовый'))
        builder.button(text='Простой чай', callback_data=Categorie(name='Простой чай'))
        builder.button(text='Личный кабинет', callback_data=Profile(back='menu'))
        builder.adjust(2, 2, 2, 1, 1)
        return builder.as_markup()


kb = Keyboard()
