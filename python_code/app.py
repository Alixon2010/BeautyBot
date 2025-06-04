import asyncio
from aiogram import Bot, Dispatcher


from dotenv import load_dotenv

from os import getenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()

async def main():
    from python_code.handlers import start_router
    bot = Bot(token=BOT_TOKEN)
    dp.include_router(start_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())