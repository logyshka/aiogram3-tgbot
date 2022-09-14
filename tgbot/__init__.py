from tgbot.loader import dp, bot
from tgbot.routers import set_routers
from tgbot.middlewares import set_middlewares
from tgbot.utils.logging import set_logging
from tgbot import handlers


__all__ = ['set_routers', 'start_bot', 'set_middlewares', 'set_logging', 'dp', 'bot']
