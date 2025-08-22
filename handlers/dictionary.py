import json
from pathlib import Path
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import client

router = Router()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def lookup_term(term: str) -> str | None:
    try:
        with open(DATA_DIR / "dictionary.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(term.lower())
    except Exception:
        return None


@router.message(Command('dictionary'))
async def dictionary(message: Message):
    raw = message.text.replace("/dictionary", "").strip()
    if not raw:
        await message.answer("Введи термін після команди. Напр.: лицева петля")
        return

    term = raw
    from_base = lookup_term(term)
    if from_base:
        await message.answer(f"<b>{term}</b>: {from_base}")
        return


    system = "Ти словник в'язальних термінів. Дай чітке коротке пояснення і 1 приклад."
    user = f"Поясни термін: {term}"
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
    )
    await message.answer(resp.choices[0].message.content)