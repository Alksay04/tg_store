import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from dotenv import dotenv_values
from users.users import read_user_config, write_user_config, update_user_config, user_exists
from keyboards.keyboards import start_keyboard, settings_keyboard
config = dotenv_values(".env")

bot = Bot(token=config["BOT_TOKEN"])
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message):
    
    
    user = message.from_user
    user_id = user.id

    if user_exists(user_id=user_id):
        user_config = read_user_config(user_id=user_id)
    else:
        user_config = {
            "first_name": user.first_name,
            "addresses": [],
            "cachback": 0,
        }
        write_user_config(user_id=user_id, config=user_config)
    await message.answer(f'Привет, {user_config["first_name"]}!',
                        reply_markup=start_keyboard())
    
@dp.callback_query(F.data == 'settings')
async def settings_menu(callback: CallbackQuery):
    await callback.message.edit_text(f'Настройки аккаунта', "{user_config} = (first_name)", 
                                     reply_markup=settings_keyboard())
    

@dp.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery):
    user_id = callback.message.chat.id
    user = read_user_config(user_id=user_id)

    await callback.message.edit_text(text=f'Добро пожаловать!', 
                                     reply_markup=start_keyboard())
    
@dp.callback_query(F.data == 'name_change')
async def name_change(callback: CallbackQuery):
    await callback.message.edit_text(text='Введите новое имя:')

@dp.message(F.text)
async def new_name(message: Message):
    new_name = message.text
    user_id = message.from_user.id
    keys_to_update = {
        'first_name': new_name
    }
    update_user_config(user_id=user_id, keys_to_update=keys_to_update)
    await message.answer(text=f'{new_name}, Вашe имя успешно изменено!')

async def main():
    print('Я запущен!')
    await dp.start_polling(bot)
    
asyncio.run(main())