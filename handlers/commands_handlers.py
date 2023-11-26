from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config.config import load_config, Config
from keyboards.keyboards import (create_pagination_kb,
                                 create_bookmarks_keyboard,
                                 create_books_keyboard)
from lexicon.lexicon import COMMANDS_RU, ANSWERS_RU
from services.database.db_connection import bot_database as db
from services.functions import save_users_id, delete_prev_messages

# Инициализация глобальных объектов
config: Config = load_config()
router = Router()
last_bot_message_id: int = 0


# =====================КОМАНДЫ=====================#

# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
    msg = await message.answer(COMMANDS_RU.start.answer)
    await save_users_id(message)

    global last_bot_message_id
    last_bot_message_id = await delete_prev_messages(bot, msg, message)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands=COMMANDS_RU.help.command))
async def process_help_command(message: Message, bot: Bot):
    msg = await message.answer(COMMANDS_RU.help.answer)
    await save_users_id(message)
    global last_bot_message_id
    last_bot_message_id = await delete_prev_messages(bot, msg, message, last_bot_message_id)


# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@router.message(Command(commands=COMMANDS_RU.beginning.command))
async def process_beginning_command(message: Message, bot: Bot):
    uid = message.from_user.id
    await save_users_id(message)

    if db.user_interface.get_books(uid):
        db.user_interface.set_current_page(uid, 1)
        page = db.user_interface.get_current_page(uid)
        book = db.user_interface.get_current_book(uid)
        text = db.book_interface.get_page_content(book, page)
        page_num = db.book_interface.get_length(book)
        msg = await message.answer(
            text=text,
            reply_markup=create_pagination_kb(page, page_num)
        )
    else:
        msg = await message.answer(text=ANSWERS_RU.no_books)

    global last_bot_message_id
    last_bot_message_id = await delete_prev_messages(bot, msg, message, last_bot_message_id)


# Этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@router.message(Command(commands=COMMANDS_RU.continue_.command))
async def process_continue_command(message: Message, bot: Bot):
    uid = message.from_user.id
    await save_users_id(message)

    if db.user_interface.get_current_book(uid):
        page = db.user_interface.get_current_page(uid)
        book = db.user_interface.get_current_book(uid)
        text = db.book_interface.get_page_content(book, page)
        page_num = db.book_interface.get_length(book)

        msg = await message.answer(
            text=text,
            reply_markup=create_pagination_kb(page, page_num)
        )
    else:
        msg = await message.answer(text=ANSWERS_RU.no_books)

    global last_bot_message_id
    last_bot_message_id = await delete_prev_messages(bot, msg, message, last_bot_message_id)


# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@router.message(Command(commands=COMMANDS_RU.bookmarks.command))
async def process_bookmarks_command(message: Message, bot: Bot):
    uid = message.from_user.id
    bookmarks = db.user_interface.get_book_marks(uid)
    await save_users_id(message)

    if bookmarks:
        msg = await message.answer(
            text=COMMANDS_RU.bookmarks.answer,
            reply_markup=create_bookmarks_keyboard(bookmarks)
        )
    else:
        msg = await message.answer(text=ANSWERS_RU.no_bookmarks)

    global last_bot_message_id
    last_bot_message_id = await delete_prev_messages(bot, msg, message, last_bot_message_id)


# Этот хэндлер будет срабатывать на команду "/books"
# и отправлять пользователю список сохраненных книг,
# если они есть или сообщение о том, что книг нет
@router.message(Command(commands=COMMANDS_RU.books.command))
async def process_books_command(message: Message, bot: Bot):
    uid = message.from_user.id
    books = db.user_interface.get_books(uid)
    await save_users_id(message)

    if books:
        msg = await message.answer(
            text=COMMANDS_RU.books.answer,
            reply_markup=create_books_keyboard(*books)
        )
    else:
        msg = await message.answer(text=ANSWERS_RU.no_books)

    global last_bot_message_id
    last_bot_message_id = await delete_prev_messages(bot, msg, message, last_bot_message_id)


# Непредусмотренные сообщения
@router.message()
async def send_echo(message: Message):
    await message.answer(f'Извините, но я не понимаю команду {message.text}. Пожалуйста, попробуйте еще раз '
                         f'или воспользуйтесь командой /help для получения дополнительной информации о '
                         f'доступных командах')
