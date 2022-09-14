from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import get_config


config = get_config()
bot = Bot(token=config.bot.token, parse_mode='html')
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler(timezone=utc)

