import logging
import asyncio
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

from config import TOKEN

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Временное хранилище доступа
user_access = {}
ACCESS_DURATION = timedelta(hours=24)

def has_access(user_id: int) -> bool:
    if user_id in user_access:
        return datetime.now() < user_access[user_id]
    return False

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_access[user_id] = datetime.now() + ACCESS_DURATION
    await message.answer("✅ Бот работает! Доступ активирован на 24 часа.")

# Команда /status
@dp.message(Command("status"))
async def cmd_status(message: Message):
    user_id = message.from_user.id
    if has_access(user_id):
        left = user_access[user_id] - datetime.now()
        hours = int(left.total_seconds() // 3600)
        minutes = int((left.total_seconds() % 3600) // 60)
        await message.answer(f"⏱ У вас остался доступ на {hours} ч {minutes} мин.")
    else:
        await message.answer("❌ Доступ истёк. Обратитесь к администратору.")

# Точка входа
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
