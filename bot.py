# импорты
import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import hello
from handlers import profile_page, story_page, contact_page, menu_page, categorie_page, drink_page, update_options

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token='6042184403:AAFVyPskvUIFFKzVM49vCtYL8VHCWCoyXLI', parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(hello.router)
    dp.include_routers(profile_page.router,
                       story_page.router,
                       contact_page.router,
                       menu_page.router,
                       categorie_page.router,
                       drink_page.router,
                       update_options.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
