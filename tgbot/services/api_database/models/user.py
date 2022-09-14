from peewee import *
from datetime import datetime
from tgbot.services.api_database.manage import BaseModel


class User(BaseModel):
    id = IntegerField(unique=True)
    username = CharField(max_length=32)
    join_date = DateTimeField(default=datetime.now())
    sub_date = DateTimeField(default=datetime.now())