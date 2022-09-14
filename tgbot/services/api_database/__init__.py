from tgbot.services.api_database.manage import db, Consts
from tgbot.services.api_database.models import User
from os.path import exists


def create_tables(again: bool = False) -> bool:
    if exists(Consts.database_file):
        return again
    elif again:
        return False
    db.create_tables(models=[User])
    return create_tables(True)


__all__ = ['User', 'create_tables']
