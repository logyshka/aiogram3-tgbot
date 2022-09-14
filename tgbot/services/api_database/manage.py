from peewee import *
from config import Consts


db = SqliteDatabase(Consts.database_file)


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)

    @classmethod
    def get_all(cls, *fields):
        if len(fields) == 0:
            return cls.select().dicts()
        else:
            return cls.select(*fields).dicts()
