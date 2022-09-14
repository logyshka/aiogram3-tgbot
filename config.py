from configparser import ConfigParser
from dataclasses import dataclass
from os.path import dirname, exists
from pickle import loads, dumps


# Basic config class
@dataclass
class Cfg:

    def __getitem__(self, item):
        return self.__dict__.get(item)

    def __setitem__(self, key, value):
        self.__dict__[key] = value


# Container of pauses beetween getting of reserve copies
@dataclass
class RcopyPauses(Cfg):
    database: int = 30


# Miscellanea container
@dataclass
class Misc(Cfg):
    rcopy_pauses: RcopyPauses = RcopyPauses()


# Bot configuration container
@dataclass
class BotConfig(Cfg):
    token: str
    admins: list


# Const variables container
@dataclass
class Consts(Cfg):
    working_dir: str = dirname(__file__)
    config_cache: str = working_dir + '/tgbot/storage/cache/config.cch'
    config_file: str = working_dir + '/config.ini'
    database_file: str = working_dir + '/tgbot/storage/database.sqlite'
    logging_dir: str = working_dir + '/tgbot/storage/logging'
    jobs_cache: str = working_dir + '/tgbot/storage/cache/jobs.cch'


# Глобальная конфигурация
@dataclass
class GlobalConfig(Cfg):
    bot: BotConfig
    consts: Consts = Consts()
    misc: Misc = Misc()

    # Сохраняет глобальную конфигурацию
    def save(self):
        with open(Consts.config_cache, 'wb') as file:
            file.write(dumps(self))


# Получает список админов из строки
def get_admins(line: str, separator: str = ','):
    return [int(admin) for admin in line.split(separator) if admin.isdigit()]


# Получает глобальную конфигурацию
def get_config() -> GlobalConfig:
    if exists(Consts.config_cache):
        with open(Consts.config_cache, 'rb') as file:
            byte_data = file.read()
            _config = loads(byte_data)
            if isinstance(_config, GlobalConfig):
                return _config

    parser = ConfigParser()
    parser.read(Consts.config_file)
    bot_section = parser['BOT']
    bot_config = BotConfig(
        token=bot_section['token'],
        admins=get_admins(bot_section['admins'])
    )

    return GlobalConfig(
        bot=bot_config
    )
