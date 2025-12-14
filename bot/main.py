import sys
import os
import asyncio
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from asgiref.sync import sync_to_async
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biotron.settings")

import django
django.setup()

from aiogram import Bot, Dispatcher
from core.models import User
logging.basicConfig(level=logging.INFO)
TOKEN = "8451161312:AAF4nxiiH4ImSNNbzB3eJcEgLyQu9C6_t0Q"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Foydalanuvchini saqlash (asyncga mos) ---
@sync_to_async
def save_user(tg_id: int, name: str):
    user, created = User.objects.get_or_create(
        tg_id=tg_id,
        defaults={"name": name}
    )
    return user

# --- /start komandasi ---
@dp.message(CommandStart())
async def StartBot(message: Message):
    tg_id = message.from_user.id
    name = message.from_user.full_name

    # Foydalanuvchini bazaga saqlash
    await save_user(tg_id, name)

    # Kanal URL
    CHANNEL_URL = "https://t.me/bio_tron_rasmiy"
    WEB_URL = f"http://127.0.0.1:8000/?id={tg_id}"

    button_pr = InlineKeyboardButton(text="Test sahifasini ochish", url=WEB_URL)
    # Faqat bitta tugma — kanalga o'tish
    button = InlineKeyboardButton(text="Telegram kanalga a'zo bo'lish", url=CHANNEL_URL)
    markup = InlineKeyboardMarkup(inline_keyboard=[[button,button_pr]])

    await message.answer(
        f"Assalomu alaykum, {name}!\n\n"
        f"\"BIOTRON\" loyihasiga xush kelibsiz!\n"
        f"Kanalimizga a'zo bo'lish uchun quyidagi tugmani bosing 👇",
        reply_markup=markup
    )




# --- Botni ishga tushirish ---
# --- Botni ishga tushirish ---
async def main():
    await bot.send_message(chat_id=5148276461, text="Bot ishga tushdi")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot to‘xtatildi.')
    except Exception as e:
        print(f'Xato: {e}')