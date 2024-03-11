# импорты
import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import hello
from handlers import profile_page, story_page, contact_page, menu_page, categorie_page, drink_page, update_options, \
    preadded_page, count_drink, busket_page, red_offer_page, admin_page, red_stop_page,zakaz_page
from texts import bot2
logging.basicConfig(level=logging.INFO)


async def main():
    dp = Dispatcher()
    dp.include_routers(hello.router)
    dp.include_routers(profile_page.router,
                       story_page.router,
                       contact_page.router,
                       menu_page.router,
                       categorie_page.router,
                       drink_page.router,
                       update_options.router,
                       preadded_page.router,
                       count_drink.router,
                       busket_page.router,
                       red_offer_page.router,
                       admin_page.router,
                       red_stop_page.router,
                       zakaz_page.router)
    await bot2.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot2)


if __name__ == "__main__":
    asyncio.run(main())
