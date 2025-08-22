import json
from pathlib import Path
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import client

router = Router()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_products():
    try:
        with open(DATA_DIR / "products.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


@router.message(Command("yarn"))
async def yarn_recommend(message: Message):
    """Користувач пише: /yarn шарф, зима, класичний"""
    raw = message.text.replace("/yarn", "").strip()
    if not raw:
        await message.answer(
            "Введи так: <b>/yarn виріб, сезон, стиль</b>\nПриклад: <i>/yarn шапка, зима, мінімалістичний</i>"
        )
        return

    try:
        item, season, style = [part.strip() for part in raw.split(",")]
    except ValueError:
        await message.answer("Будь ласка, три параметри через кому: виріб, сезон, стиль")
        return

    base_products = load_products()

    system = (
        "Ти консультант з пряжі. На основі виробу/сезону/стилю дай 3–5 варіантів пряжі. "
        "Кожен варіант: назва (якщо в каталозі — використовуй), склад, метраж/товщина, чому підходить, порада по кольору."
    )
    catalog_snippet = json.dumps(base_products.get("yarns", [])[:20], ensure_ascii=False)

    user = (
        f"Виріб: {item}; Сезон: {season}; Стиль: {style}. "
        f"Можеш орієнтуватися на такий каталог (якщо доречно): {catalog_snippet}"
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.8,
    )

    text = resp.choices[0].message.content
    await message.answer(text)