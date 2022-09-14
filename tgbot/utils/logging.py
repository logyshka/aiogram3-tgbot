from loguru import logger
from config import Consts
from aiogram import types
from tgbot.utils.misc_functions import create_archive_from_dir


# Настройка логирования
def set_logging():
    logger.add(Consts.logging_dir + '/bot_log.txt', rotation='1 day')


# Получить архив с логами
def get_logging_archive() -> types.BufferedInputFile:
    archive = create_archive_from_dir(Consts.logging_dir, 'Тута логи как бы да!')
    return types.BufferedInputFile(archive, 'logs.rar')
