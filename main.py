from aiogram import Dispatcher, Bot
import logging
import asyncio
from handlers import router
import db
TOKEN = "6448625821:AAECe0YGWT0eh3uOTpfpRVj6w6KtHMSgLO4"
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def start():
    dp.include_router(router=router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())