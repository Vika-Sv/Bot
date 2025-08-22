from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config import client

router = Router()

ALLOWED = {"шарф", "шапка", "снуд"}


@router.message(Command("instr"))
async def make_instruction(message: Message):
    raw = message.text.replace("/instr", "").strip().lower()
    if not raw or raw not in ALLOWED:
        await message.answer("Вибери виріб: /instr шарф | шапка | снуд")
        return

    system = (
        "Ти майстер в'язання. Зроби покрокову інструкцію для вибраного виробу, "
        "з урахуванням базового рівня. Додай поради по спицях/гачку, пряжі і щільності."
    )
    user = f"Виріб: {raw}"

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.6,
    )

    await message.answer(resp.choices[0].message.content)