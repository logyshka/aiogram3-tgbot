from aiogram import types
from aiogram.fsm.context import FSMContext
from tgbot.routers import user_router
from tgbot.services.api_database import User


router = user_router


async def start_handler(msg: types.Message, state: FSMContext, user: User):
    await state.clear()

    if user is None:
        User.create(id=msg.from_user.id, username=msg.from_user.username)

    text = 'Хаюшки'
    await msg.answer(text=text)


@router.message(commands='start', state='*')
async def start(msg: types.Message, state: FSMContext, user: User):
    await start_handler(msg, state, user)
