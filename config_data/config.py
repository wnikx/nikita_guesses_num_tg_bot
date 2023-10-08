from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    bot_token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path):
    env = Env()

    env.read_env()

    return Config(TgBot(bot_token=env('BOT_TOKEN'),
                        admin_ids=list(map(int, env.list('ADMIN_IDS')))))
