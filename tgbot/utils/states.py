from aiogram.fsm.state import State, StatesGroup


# Admin states group
class Admin(StatesGroup):
    mailing = State()
    buttoning = State()
    adding_admin = State()