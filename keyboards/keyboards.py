from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(test="Настройки", callback_data='settings'))
    return builder.as_markup()
