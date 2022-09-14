from aiogram import Bot
from loguru import logger
from tgbot.services.api_database import create_tables
from tgbot.utils.admin_functions import replan_rcopy_database
from tgbot.loader import scheduler, config


# Действия при запуске бота
async def on_startup(bot: Bot):
    if create_tables():
        logger.success('База данных успешно создана!')
        logger.success('Таблицы в БД успешно созданы!')

    bot_info = await bot.me()
    logger.opt(colors=True).info(f'Бот запущен. Username: <blue>@{bot_info.username}</blue>')
    scheduler.start()
    replan_rcopy_database()


# Действия при выключении бота
async def on_shutdown():
    ...


