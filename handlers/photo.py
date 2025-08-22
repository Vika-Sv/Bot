import json
from aiogram.filters import Command
from pathlib import Path
import base64
from aiogram import Router, F
from aiogram.types import Message, ContentType
from config import client

router = Router()


@router.message(F.content_type == ContentType.PHOTO)
async def explain_chart_symbols(message: Message):
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_bytes = await message.bot.download_file(file.file_path)

    b64 = base64.b64encode(file_bytes.getvalue()).decode()
    data_url = f"data:image/jpeg;base64,{b64}"

    system = (
        "Ти експерт з читання в'язальних схем. Розпізнай основні символи на зображенні, "
        "зістав їх з типовими значеннями і коротко поясни, як в'язати цей фрагмент."
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Поясни символи на цій схемі і опиши візерунок."},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            },
        ],
        temperature=0.3,
    )

    await message.answer(resp.choices[0].message.content)