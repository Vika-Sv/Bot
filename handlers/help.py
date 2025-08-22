from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config import client

router = Router()


@router.message(Command("help"))
async def fix_problems(message: Message):
    text = message.text.replace("/help", "").strip()
    if not text:
        await message.answer(
            "Опиши проблему після команди. Напр.:краї скручуються, петлі різні по висоті"
        )
        return

    system = (
        "Ти майстер, який допомагає вирішувати типові проблеми у в'язанні. "
        "Дай 2–4 способи вирішення і 2 поради як уникнути цього в майбутньому."
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ],
        temperature=0.5,
    )

    await message.answer(resp.choices[0].message.content)