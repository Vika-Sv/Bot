# bot.py — точка входу. Тут я збираю всіх хендлерів і запускаю бота.
# Пишу максимально просто і зрозуміло, як першокурсник :) 

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from config import TELEGRAM_TOKEN


from handlers.recomendation import router as recomendation_router
from handlers.dictionary import router as dictionary_router
from handlers.instruction import router as instruction_router
from handlers.calc import router as calc_router
from handlers.photo import router as photo_router
from handlers.help import router as help_router


logging.basicConfig(level=logging.INFO)

dp = Dispatcher()

dp.include_router(help_router)
dp.include_router(dictionary_router)
dp.include_router(recomendation_router)
dp.include_router(instruction_router)
dp.include_router(calc_router)
dp.include_router(photo_router)


@dp.message(CommandStart())
async def on_start(message: Message):
    text = ('Привіт! Рада тебе бачити сьогодні')
    await message.answer(text)


async def main() -> None:
    bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if name == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")