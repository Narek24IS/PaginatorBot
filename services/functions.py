from aiogram import Bot
from aiogram.types import Message

from config.config import load_config, Config
from services.database.db_connection import bot_database

config: Config = load_config()


def load_users_id() -> list[int]:
    return list(bot_database.get_table_data_as_dict('users').keys())


# Восстановление ИД пользователей
# Сохранение ИД пользователей в файл
async def save_users_id(message: Message) -> list[int]:
    sender_id = message.from_user.id
    users_id = load_users_id()

    if message.from_user.id not in users_id:
        print(f'Пользователь {message.from_user.username} сохранён')
        bot_database.user_interface.create_if_not_exists(sender_id, 1, 1, [1, 2, 3, 4, 5], dict())

    return load_users_id()


async def delete_prev_messages(bot: Bot, bot_message: Message, user_message: Message = None,
                               last_bot_message_id: int = 0) -> int:
    if user_message:
        await bot.delete_message(chat_id=user_message.chat.id, message_id=user_message.message_id)
    if last_bot_message_id:
        await bot.delete_message(chat_id=bot_message.chat.id, message_id=last_bot_message_id)
    return bot_message.message_id
