from aiogram.fsm.state import State, StatesGroup

class SettingStates(StatesGroup):
    choose_name = State()
    add_address = State()
