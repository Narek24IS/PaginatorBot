from services.database.db_connection import bot_database
from aiogram.types import Message
from config.config import load_config, Config

config: Config = load_config()

def load_users_id() -> list[int]:
    return list(bot_database.get_table_data_as_dict('users').keys())

# users_id = load_users_id()


# Восстановление ИД пользователей
# Сохранение ИД пользователей в файл
async def save_users_id(message: Message) -> list[int]:
    sender_id = message.from_user.id
    users_id = load_users_id()

    if message.from_user.id not in users_id:
        print(f'Пользователь {message.from_user.username} сохранён')
        bot_database.user_interface.create_if_not_exists(sender_id, 1, 1, [1,2,3,4,5], dict())

    return load_users_id()




