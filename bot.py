# импорты
import asyncio
from aiogram import F
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config_reader import config
from random import randint
from handlers import hello,dimas_page
from callbacks import *
'''
отправка зипархивов для Димы с фотками
получение полной инфы по заказам
скипанием заказов стрелками, отдельный поиск по номеру заказа




'''

logging.basicConfig(level=logging.INFO)



# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value(),parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(hello.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())