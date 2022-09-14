import typing
from peewee import *
from tgbot.services.api_database.manage import BaseModel


# Model that helps to create couples of users
class Couple(BaseModel):
    couple_id = IntegerField(primary_key=True)
    user_id1 = IntegerField()
    user_id2 = IntegerField(default=0)

    @classmethod
    def get_user_couple(cls, user_id: int) -> typing.Self:
        couple = cls.get_or_none(user_id1=user_id)
        if couple is None:
            couple = cls.get_or_none(user_id2=user_id)
        return couple

    @classmethod
    def enter_couple(cls, user_id: int) -> None:
        couple = cls.get_user_couple(user_id)

        if couple is not None:
            raise Exception

        vacant_couple = Couple.get_or_none(user_id2=0)

        if vacant_couple is None:
            Couple.create(user_id1=user_id)

        else:
            vacant_couple.user_id2 = user_id

    @classmethod
    def leave_couple(cls, user_id: int) -> None:
        couple = cls.get_user_couple(user_id)
        if couple is not None:
            couple.delete()