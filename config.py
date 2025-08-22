import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv('.env')

TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN is missing in .env")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing in .env")


client = OpenAI(api_key=OPENAI_API_KEY)