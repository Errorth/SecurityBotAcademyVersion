import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv

import db
from handlers import router
async def main():
    TOKEN = getenv("TOKEN")
    bot = Bot(token="6448625821:AAECe0YGWT0eh3uOTpfpRVj6w6KtHMSgLO4", parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    asyncio.run(main())