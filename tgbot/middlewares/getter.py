import typing
from aiogram import BaseMiddleware
from aiogram import types
from tgbot.services.api_database import User
from loguru import logger


class GetterMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: typing.Callable[
                [types.TelegramObject, typing.Dict[str, typing.Any]], typing.Awaitable[typing.Any]],
            event: typing.Union[types.Message, types.CallbackQuery],
            data: typing.Dict[str, typing.Any]
    ) -> typing.Any:

        if isinstance(event, (types.Message, types.CallbackQuery)):
            data['user'] = User.get_or_none(id=event.from_user.id)

        result = await handler(event, data)

        return result
