from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Каталог", callback_data='catalogue'),
                InlineKeyboardButton(text="Настройки", callback_data='settings'))
    return builder.as_markup()

def settings_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text='Поменять имя', callback_data='name_change'),
        InlineKeyboardButton(text='Добавить адрес', callback_data='address'),
        InlineKeyboardButton(text='Вернуться в меню', callback_data='back_to_menu')
    )
    builder.adjust(2, 1)
    return builder.as_markup()

def addresses_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text='Добавить адрес', callback_data='add_address'),
        InlineKeyboardButton(text='Вернуться в меню', callback_data='back_to_menu')
    )

    builder.adjust(1)
    return builder.as_markup()

def back_to_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='back_to_menu'))
    return builder.as_markup()


def catalogue_keyboard(wares):
    builder = InlineKeyboardBuilder()

    for ware in wares:
        builder.add(InlineKeyboardBuilder(text=ware.name, callback_data=f'ware_{ware.id}'))

    builder.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='back_to_menu'))
    builder.adjust(1)
    return builder.as_markup()