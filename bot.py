import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from dotenv import dotenv_values
from users.users import read_user_config, write_user_config, update_user_config, user_exists
from keyboards.keyboards import start_keyboard, settings_keyboard, addresses_keyboard
from states.states import SettingStates
from users.address import Address

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
async def name_change(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Введите новое имя:')

    await state.set_state(SettingStates.choose_name)

@dp.message(F.text, SettingStates)
async def new_name(message: Message, state: FSMContext):
    new_name = message.text
    user_id = message.from_user.id
    keys_to_update = {
        'first_name': new_name
    }
    update_user_config(user_id=user_id, keys_to_update=keys_to_update)
    await message.answer(text=f'{new_name}, Вашe имя успешно изменено!')
    await state.set_state(None)

@dp.callback_query(F.data=="addresses_settings")
async def addresses_settings(callback: CallbackQuery, state: FSMContext):
    user_id = callback.message.chat.id
    config = read_user_config(user_id=user_id)

    if len(config['addresses']) == 0:
        await callback.message.edit_text('У вас не указан ни один адрес доставки.\nДобавьте адреса ниже:', 
                                         reply_markup=addresses_keyboard())

    await callback.message.edit_text('',)

@dp.callback_query(F.data=='add_address')
async def add_addresses(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите название нового адреса:')
    await state.set_state(SettingStates.add_address_label)

@dp.message(F.text, SettingStates)
async def add_address_label(message: Message, state: FSMContext):
    address_label = message.text

    await message.answer(f'Укажите адрес для {address_label}')
    await state.set_state(SettingStates.add_address_text)
    await state.set_data('label': address_label)

@dp.message(F.text, SettingStates.add_address_text)
async def add_address_text(message: Message, state: FSMContext):
    address = message.text

    data = await state.get_data()
    address_label = data('label')

    user_id = message.from_user.id
    config = read_user_config(user_id=user_id)

    new_address = Address.fron_dict(
        {
            "label": address_label,
            "address": address
        }
    )

    config['addresses'].append(new_address.to_dict())
    keys_to_update = {
        'addresses': config['addresses']
    }
    update_user_config(user_id=user_id, keys_to_update=keys_to_update)

async def main():
    print('Я запущен!')
    await dp.start_polling(bot)
    
asyncio.run(main())