import typing
from aiogram import types
from aiogram.filters import BaseFilter


class IsAdmin(BaseFilter):
    admins: list[int]

    async def __call__(self, obj: typing.Union[types.CallbackQuery, types.Message]):
        if isinstance(obj, (types.Message, types.CallbackQuery)):
            return obj.from_user.id in self.admins
        return False
