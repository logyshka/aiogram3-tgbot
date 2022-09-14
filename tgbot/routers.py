from aiogram import Router
from tgbot.loader import dp, config
from tgbot.utils.filters import IsAdmin

user_router = Router(name='user')

is_admin = IsAdmin(admins=config.bot.admins)
admin_router = Router(name='admin')
admin_router.message.filter(is_admin)
admin_router.callback_query.filter(is_admin)


def set_routers() -> None:
    dp.include_router(user_router)
    dp.include_router(admin_router)
