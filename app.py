import asyncio
from aiogram import Bot, Dispatcher
from bot.router import router
from config import TELEGRAM_TOKEN

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(token=TELEGRAM_TOKEN)
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"]) 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
