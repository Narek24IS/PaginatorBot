import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import load_config, Config
from config.config_bot import set_main_menu
from handlers import commands_handlers, bookmarks_handlers, books_handlers
from services.database.setup_db import setup_db

logger = logging.getLogger(__name__)


async def main() -> None:
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Создаём таблицы, если их нет
    setup_db(new=False)

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Настройка меню с командами
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_router(books_handlers.router)
    dp.include_router(bookmarks_handlers.router)
    dp.include_router(commands_handlers.router)


# Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
