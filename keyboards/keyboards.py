from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup

from keyboards.keyboard_builders import InlineKeyboard
from lexicon.lexicon import INLINE_BUTTONS_RU
from services.database.db_connection import bot_database as db
from callback_factories.edit_menu import BookCallbackFactory, BookmarksCallbackFactory


def create_pagination_kb(page_number, total_pages) -> InlineKeyboardMarkup:
    return InlineKeyboard(INLINE_BUTTONS_RU.backward,
                          f'{page_number}/{total_pages}',
                          INLINE_BUTTONS_RU.forward)(3)


def create_bookmarks_keyboard(bookmarks: dict[str:list[int]]) -> InlineKeyboardMarkup:
    # Создаем список кнопок
    buttons: list[InlineKeyboardButton] = []
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for book_name, pages in bookmarks.items():
        book = db.book_interface.get_content(book_name)
        if book:
            for page_num in pages:
                buttons.append(InlineKeyboardButton(
                    text=f'{book_name}: {page_num} - {book[str(page_num)][:100]}',
                    callback_data=BookmarksCallbackFactory(book_name=book_name,
                                                           page_num=page_num, choose=True).pack()
                ))
    # Добавляем в клавиатуру в конце две кнопки "Редактировать"
    last_row = [
        InlineKeyboardButton(
            text=INLINE_BUTTONS_RU.edit_bookmarks,
            callback_data=INLINE_BUTTONS_RU.edit_bookmarks
        )]
    return InlineKeyboard(*buttons, last_row=last_row)(1)


def create_bookmarks_edit_keyboard(bookmarks: dict[str:list[int]]) -> InlineKeyboardMarkup:
    # Создаем список кнопок
    buttons: list[InlineKeyboardButton] = []
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for book_name, pages in bookmarks.items():
        book = db.book_interface.get_content(book_name)
        for page_num in pages:
            buttons.append(InlineKeyboardButton(
                text=f'{INLINE_BUTTONS_RU.del_}{book_name}: {page_num} - {book[str(page_num)][:100]}',
                callback_data=BookmarksCallbackFactory(book_name=book_name,
                                                       page_num=page_num, delete=True).pack()
            ))
    # Добавляем в конец клавиатуры кнопку "Отменить"
    last_row = [
        InlineKeyboardButton(
            text=INLINE_BUTTONS_RU.edit_bookmarks_cancel,
            callback_data=INLINE_BUTTONS_RU.edit_bookmarks_cancel
        )]

    return InlineKeyboard(*buttons, last_row=last_row)(1)


def create_books_keyboard(*args: str) -> InlineKeyboardMarkup:
    # Создаем список кнопок
    buttons: list[InlineKeyboardButton] = []
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for book_name in sorted(args):
        buttons.append(InlineKeyboardButton(
            text=book_name,
            callback_data=BookCallbackFactory(book_name=book_name, choose=True).pack()
        ))
    # Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
    last_row = [
        InlineKeyboardButton(
            text=INLINE_BUTTONS_RU.edit_books,
            callback_data=INLINE_BUTTONS_RU.edit_books
        )]
    return InlineKeyboard(*buttons, last_row=last_row)(1)


def create_books_edit_keyboard(*args: str) -> InlineKeyboardMarkup:
    # Создаем список кнопок
    buttons: list[InlineKeyboardButton] = []
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for book_name in sorted(args):
        buttons.append(InlineKeyboardButton(
            text=INLINE_BUTTONS_RU.del_ + book_name,
            callback_data=BookCallbackFactory(book_name=book_name, delete=True).pack()
        ))
    # Добавляем в конец клавиатуры кнопку "Отменить"
    last_row = [
        InlineKeyboardButton(
            text=INLINE_BUTTONS_RU.edit_books_cancel,
            callback_data=INLINE_BUTTONS_RU.edit_books_cancel
        )]

    return InlineKeyboard(*buttons, last_row=last_row)(1)
