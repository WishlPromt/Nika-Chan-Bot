import asyncio
import logging

from aiogram import Bot, Dispatcher

from system.config import TOKEN
from app.handlers.main_handlers import router as main_router
from app.handlers.cards_handlers import router as cards_router
from app.handlers.inventory_handlers import router as inventory_router
from app.handlers.votes_handlers import router as votes_router

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_routers(main_router, inventory_router, cards_router, votes_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    logging.basicConfig(level=logging.INFO)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('close')
