import asyncio
from tgbot import register_routers, set_middlewares, set_logging
from tgbot.loader import dp, bot
from tgbot.utils.on_events import on_startup, on_shutdown


# Запускает бота
def start_bot():
    register_routers()
    set_middlewares()
    set_logging()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    start_bot()
