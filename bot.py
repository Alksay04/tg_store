import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message
from dotenv import dotenv_values
from users.users import read_user_config, write_user_config
from keyboards.keyboards import start_keyboard
config = dotenv_values(".env")

bot = Bot(token=config["BOT_TOKEN"])
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message):
    
    
    user = message.from_user
    user_id = user.id
    user_config = {
        "first_name": user.first_name,
        "addresses": [],
        "cachback": 0,
    }
    write_user_config(user_id=user_id, config=user_config)
    await message.reply(f'Привет, {user.first}!',
                        reply_markup=start_keyboard())
async def main():
    print('Я запущен!')
    await dp.start_polling(bot)
    
asyncio.run(main())