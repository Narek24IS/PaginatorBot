from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import (create_pagination_kb,
                                 create_bookmarks_keyboard,
                                 create_bookmarks_edit_keyboard, create_books_keyboard, create_books_edit_keyboard)
from config.config import load_config, Config
from services.functions import load_users_id, save_users_id
from services.database.db_connection import bot_database as db
from lexicon.lexicon import COMMANDS_RU, ANSWERS_RU, INLINE_BUTTONS_RU
from filtres.filtres import IsBookmarkCallbackData, IsDigitCallbackData, IsDelBookmarkCallbackData, IsBookCallbackData, \
    IsDelBookCallbackData
from services.book import Book

# Инициализация глобальных объектов
config: Config = load_config()
router = Router()

#=====================КОМАНДЫ=====================#

# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(COMMANDS_RU.start.answer)
    await save_users_id(message)

# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands=COMMANDS_RU.help.command))
async def process_help_command(message: Message):
    await message.answer(COMMANDS_RU.help.answer)

# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@router.message(Command(commands=COMMANDS_RU.beginning.command))
async def process_beginning_command(message: Message):
    uid = message.from_user.id
    if db.user_interface.get_books(uid):
        db.user_interface.set_current_page(uid, 1)
        page = db.user_interface.get_current_page(uid)
        book = db.user_interface.get_current_book(uid)
        text = db.book_interface.get_page_content(book, page)
        page_num = db.book_interface.get_length(book)
        await message.answer(
            text=text,
            reply_markup=create_pagination_kb(page, page_num)
        )
    else:
        await message.answer(text=ANSWERS_RU.no_books)


# Этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@router.message(Command(commands=COMMANDS_RU.continue_.command))
async def process_continue_command(message: Message):
    uid = message.from_user.id
    if db.user_interface.get_current_book(uid):
        page = db.user_interface.get_current_page(uid)
        book = db.user_interface.get_current_book(uid)
        text = db.book_interface.get_page_content(book, page)
        page_num = db.book_interface.get_length(book)

        await message.answer(
            text=text,
            reply_markup=create_pagination_kb(page, page_num)
        )
    else:
        await message.answer(text=ANSWERS_RU.no_books)


# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@router.message(Command(commands=COMMANDS_RU.bookmarks.command))
async def process_bookmarks_command(message: Message):
    uid = message.from_user.id
    book = db.user_interface.get_current_book(uid)
    bookmarks = db.user_interface.get_book_marks(uid).get(book)


    if bookmarks:
        await message.answer(
            text=COMMANDS_RU.bookmarks.answer,
            reply_markup=create_bookmarks_keyboard(book, *bookmarks)
        )
    else:
        await message.answer(text=ANSWERS_RU.no_bookmarks)

# Этот хэндлер будет срабатывать на команду "/books"
# и отправлять пользователю список сохраненных книг,
# если они есть или сообщение о том, что книг нет
@router.message(Command(commands=COMMANDS_RU.books.command))
async def process_books_command(message: Message):
    uid = message.from_user.id
    # page = db.user_interface.get_current_page(uid)
    # book = db.user_interface.get_current_book(uid)
    books = db.user_interface.get_books(uid)

    if books:
        await message.answer(
            text=COMMANDS_RU.books.answer,
            reply_markup=create_books_keyboard(*books)
        )
    else:
        await message.answer(text=ANSWERS_RU.no_books)

#=====================ЧТЕНИЕ=====================#

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(F.data == INLINE_BUTTONS_RU.forward)
async def process_forward_press(callback: CallbackQuery):
    uid = callback.from_user.id
    page = db.user_interface.get_current_page(uid)
    book = db.user_interface.get_current_book(uid)
    page_num = db.book_interface.get_length(book)

    if page < page_num:
        page += 1
        db.user_interface.set_current_page(uid, page)
        text = db.book_interface.get_page_content(book, page)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(page, page_num)
        )
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(F.data == INLINE_BUTTONS_RU.backward)
async def process_backward_press(callback: CallbackQuery):
    uid = callback.from_user.id
    page = db.user_interface.get_current_page(uid)
    book = db.user_interface.get_current_book(uid)
    page_num = db.book_interface.get_length(book)

    if page > 1:
        page -= 1
        db.user_interface.set_current_page(uid, page)
        text = db.book_interface.get_page_content(book, page)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(page, page_num)
        )
    await callback.answer()


#=====================КНИГИ=====================#

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@router.callback_query(IsDelBookCallbackData())
async def process_del_book_press(callback: CallbackQuery, del_book:str):
    uid = callback.from_user.id
    db.user_interface.remove_book(uid, del_book)
    books = db.user_interface.get_books(uid)

    if books:
        await callback.message.edit_text(
            text=INLINE_BUTTONS_RU.edit_books,
            reply_markup=create_books_edit_keyboard(*books)
        )
    else:
        await callback.message.edit_text(text=ANSWERS_RU.no_bookmarks)
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@router.callback_query(IsBookCallbackData())
async def process_book_press(callback: CallbackQuery, user_book:str):
    uid = callback.from_user.id
    db.user_interface.set_current_book(uid, user_book)
    db.user_interface.set_current_page(uid, 1)
    page = db.user_interface.get_current_page(uid)
    book = db.user_interface.get_current_book(uid)
    text = db.book_interface.get_page_content(book, page)
    page_num = db.book_interface.get_length(book)
    await callback.message.answer(
        text=text,
        reply_markup=create_pagination_kb(page, page_num)
    )

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(F.data == INLINE_BUTTONS_RU.edit_books)
async def process_books_edit_press(callback: CallbackQuery):
    uid = callback.from_user.id
    books = db.user_interface.get_books(uid)


    await callback.message.edit_text(
        text=INLINE_BUTTONS_RU.edit_books,
        reply_markup=create_books_edit_keyboard(*books)
    )
    await callback.answer()


@router.message(F.data == INLINE_BUTTONS_RU.edit_books_cancel)
async def process_edit_books_cancel(callback: CallbackQuery):
    uid = callback.from_user.id
    books = db.user_interface.get_books(uid)


    await callback.message.edit_text(
        text=INLINE_BUTTONS_RU.edit_books,
        reply_markup=create_books_keyboard(*books)
    )
    await callback.answer()


@router.message(F.document)
async def process_load_book(message: Message):
    if message.document.mime_type == 'text/plain':
        book = Book(message.document)
        book_name = message.caption if message.caption else book.title
        if db.user_interface.book_exists(message.from_user.id, book_name):
            await message.answer(ANSWERS_RU.book_exist)
        else:
            content = book.get_json_text()
            uid = message.from_user.id
            db.user_interface.save_book(uid, book_name, content)
            if not db.user_interface.get_current_book(uid):
                db.user_interface.set_current_book(uid, book_name)
            await message.answer(f'Книга успешно сохранена под именем "{book_name}"')
    else:
        await message.answer(f'Неизвестный формат файла, нужен формат *.txt')


#=====================ЗАКЛАДКИ=====================#

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
@router.callback_query(IsBookmarkCallbackData())
async def process_page_press(callback: CallbackQuery):
    uid = callback.from_user.id
    page = db.user_interface.get_current_page(uid)
    book = db.user_interface.get_current_book(uid)
    db.user_interface.add_book_mark(uid, book, page)

    await callback.answer(f'Страница {page} добавлена в закладки!')

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    uid = callback.from_user.id
    book = db.user_interface.get_current_book(uid)
    page = int(callback.data)
    page_num = db.book_interface.get_length(book)
    text = db.book_interface.get_page_content(book, page)
    db.user_interface.set_current_page(uid, page)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_kb(page, page_num)
    )
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(F.data == INLINE_BUTTONS_RU.edit_bookmarks)
async def process_bookmarks_edit_press(callback: CallbackQuery):
    uid = callback.from_user.id
    book = db.user_interface.get_current_book(uid)
    bookmarks = db.user_interface.get_book_marks(uid).get(book)


    await callback.message.edit_text(
        text=INLINE_BUTTONS_RU.edit_bookmarks,
        reply_markup=create_bookmarks_edit_keyboard(book, *bookmarks)
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    uid = callback.from_user.id
    book = db.user_interface.get_current_book(uid)
    bookmark = int(callback.data[:-3])
    db.user_interface.remove_book_mark(uid, book, bookmark)
    bookmarks = dict()
    bookmarks = db.user_interface.get_book_marks(uid).get(book)


    if bookmarks:
        await callback.message.edit_text(
            text='/'+COMMANDS_RU.bookmarks.command,
            reply_markup=create_bookmarks_edit_keyboard(book, *bookmarks)
        )
    else:
        await callback.message.edit_text(text=ANSWERS_RU.no_bookmarks)
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(F.data == INLINE_BUTTONS_RU.edit_bookmarks_cancel)
async def process_bookmarks_edit_press(callback: CallbackQuery):
    uid = callback.from_user.id
    book = db.user_interface.get_current_book(uid)
    bookmarks = db.user_interface.get_book_marks(uid).get(book)


    await callback.message.edit_text(
        text=INLINE_BUTTONS_RU.edit_bookmarks,
        reply_markup=create_bookmarks_keyboard(book, *bookmarks)
    )
    await callback.answer()


# Непредусмотренные сообщения
@router.message()
async def send_echo(message: Message):
    await message.answer(f'Извините, но я не понимаю команду {message.text}. Пожалуйста, попробуйте еще раз '
                         f'или воспользуйтесь командой /help для получения дополнительной информации о '
                         f'доступных командах')
