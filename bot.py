# импорты
import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import hello


logging.basicConfig(level=logging.INFO)



async def main():
    bot = Bot(token='6061997002:AAHKvHLtZ7EnSNl73ycRkAick2zXICVuln0',parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(hello.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())