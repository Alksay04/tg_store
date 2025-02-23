from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Настройки", callback_data='settings'))
    return builder.as_markup()

def settings_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text='Поменять имя', callback_data='name_change'),
        InlineKeyboardButton(text='Изменить адрес', callback_data='addresses'),
        InlineKeyboardButton(text='Вернуться в меню', callback_data='back_to_menu')
    )
    builder.adjust(2, 1)
    return builder.as_markup()