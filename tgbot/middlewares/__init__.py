from tgbot.middlewares.getter import GetterMiddleware
from tgbot.loader import dp


# Устанавливает мидлвари
def set_middlewares() -> None:
    dp.message.middleware(GetterMiddleware())
    dp.callback_query.middleware(GetterMiddleware())
