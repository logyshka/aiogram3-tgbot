from aiogram.fsm.state import State, StatesGroup


class Admin(StatesGroup):
    mailing = State()
    buttoning = State()
    adding_admin = State()