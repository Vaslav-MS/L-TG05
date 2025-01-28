import asyncio, random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()








async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())