import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import load_config, Config
from handlers import other_handlers, user_handlers
from keyboards.set_menu import set_main_menu


async def main() -> None:
    config: Config = load_config('.env')

    bot = Bot(token=config.tg_bot.bot_token)
    dp = Dispatcher()

    dp.include_router(user_handlers.rt)

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
