# bot.py — точка входу. Тут я збираю всіх хендлерів і запускаю бота.
# Пишу максимально просто і зрозуміло, як першокурсник :) 

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from config import TELEGRAM_TOKEN

# Імпортую роутери з папки handlers
from handlers.recomandation import router as recomandation_router
from handlers.dictionary import router as dictionary_router
from handlers.instruction import router as instruction_router
from handlers.calc import router as calc_router
from handlers.photo import router as photo_router
from handlers.help import router as help_router

# Налаштовую базове логування, щоб бачити помилки і що взагалі відбувається
logging.basicConfig(level=logging.INFO)

# Створюю Dispatcher — це "мозок" aiogram, куди я підключу всі роутери
dp = Dispatcher()

# Реєструю роутери (кожен відповідає за свою фічу)
dp.include_router(help_router)
dp.include_router(dictionary_router)
dp.include_router(recomandation_router)
dp.include_router(instruction_router)
dp.include_router(calc_router)
dp.include_router(photo_router)


# Прості старт/пінг-команди прямо тут, щоб було під рукою
@dp.message(CommandStart())
async def on_start(message: Message):
    text = (
        "Привіт! Я 🧶 AI-помічник для в'язання.\n"
        "Ось що вмію:\n"
        "• /yarn — рекомендую пряжу (формат: виріб, сезон, стиль)\n"
        "• /instr — інструкція (шарф/шапка/снуд)\n"
        "• /calc — калькулятор петель (виріб, см, щільність п/см)\n"
        "• /dictionary — словник термінів\n"
        "• Надішли фото схеми — поясню символи\n"
        "• /fix — допомога з проблемами у в'язанні\n"
        "• /help — коротка довідка\n"
    )
    await message.answer(text)

@dp.message(Command("ping"))
async def ping(message: Message):
    await message.answer("pong ✨")


async def main() -> None:
    bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")