import sqlite3
import requests
from aiogram.types import Message
from config.config import load_config, Config
config: Config = load_config()


def load_users_id() -> list[int]:
    with sqlite3.connect(f"../{config.db.database}.db") as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY UNIQUE,
                    username TEXT,
                    name TEXT
                )''')

        cursor.execute("SELECT * FROM users")
        users_id_list:list[int] = [row[0] for row in cursor.fetchall()]

    return users_id_list


# users_id = load_users_id()
users_id = load_users_id()


# Восстановление ИД пользователей
# Сохранение ИД пользователей в файл
async def save_users_id(message: Message) -> list[int]:
    name = message.from_user.first_name
    sender_id = message.from_user.id
    username = message.from_user.username
    global users_id

    print(f'{message.from_user.first_name}: {message.text}')
    with sqlite3.connect(f"../{config.db.database}.db") as connection:
        cursor = connection.cursor()
        try:
            # Начинаем транзакцию автоматически
            with connection:
                if sender_id not in users_id:
                    cursor.execute("INSERT INTO users (id, username, name) VALUES (?, ?, ?)",
                                   (sender_id, username, name))
                    print('ИД сохранён')
                    connection.commit()

            return load_users_id()

        except Exception as ex:
            # Ошибки будут приводить к автоматическому откату транзакции
            print(ex)
            print('Ошибка при сохранении ИД')
            return load_users_id()


