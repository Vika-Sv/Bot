from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


TIP = (
    "Формула: петлі = розмір (у см) × щільність (п/см).\n"
    "Для светрів та шапок додаємо 2–3 см свободи. Для візерунку з косами — +10%."
)


@router.message(Command("calc"))
async def calc_stitches(message: Message):
    raw = message.text.replace("/calc", "").strip().lower()
    if not raw:
        await message.answer(
            "Формат: /calc виріб, розмір_см, щільність_п/см, [коси/без_кос]\n"
            "Приклад: /calc светр, 92, 2.4, коси\n\n" + TIP
        )
        return

    parts = [p.strip() for p in raw.split(",")]
    if len(parts) < 3:
        await message.answer("Будь ласка, щонайменше три параметри: виріб, см, щільність")
        return

    item = parts[0]
    try:
        size_cm = float(parts[1].replace(",", "."))
        density = float(parts[2].replace(",", "."))
    except ValueError:
        await message.answer("Розмір і щільність мають бути числами")
        return

    has_cables = False
    if len(parts) >= 4 and "кос" in parts[3]:
        has_cables = True


    stitches = size_cm * density

    
    if any(word in item for word in ["светр", "кофта", "кардиган", "шапка"]):
        stitches *= 1.03  

    if has_cables:
        stitches *= 1.10 

    result = round(stitches)

    note = ""
    if has_cables:
        note += "\n+ Ураховано візерунок з косами (+10%)."
    if any(word in item for word in ["светр", "кофта", "кардиган", "шапка"]):
        note += "\n+ Додана свобода облягання ~3%."

    await message.answer(
        f"{item.title()}: приблизно <b>{result}</b> петель.\n{TIP}{note}"
    )