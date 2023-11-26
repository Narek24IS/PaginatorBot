from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from filtres.filtres import IsBookCallbackData, IsDelBookCallbackData
from keyboards.keyboards import (create_pagination_kb, create_books_keyboard, create_books_edit_keyboard)
from lexicon.lexicon import COMMANDS_RU, ANSWERS_RU, INLINE_BUTTONS_RU
from services.book import Book
from services.database.db_connection import bot_database as db
from services.functions import save_users_id
from callback_factories.edit_menu import BookCallbackFactory


router = Router()


# =====================ЧТЕНИЕ=====================#

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


# =====================КНИГИ=====================#

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с книгой из списка книг к удалению
@router.callback_query(BookCallbackFactory.filter(F.delete == True))
async def process_del_book_press(callback: CallbackQuery, callback_data: BookCallbackFactory):
    uid = callback.from_user.id
    db.user_interface.remove_book(uid, callback_data.book_name)
    books = db.user_interface.get_books(uid)

    if books:
        await callback.message.edit_text(
            text=ANSWERS_RU.books_edit_menu_title,
            reply_markup=create_books_edit_keyboard(*books)
        )
    else:
        await callback.message.edit_text(text=ANSWERS_RU.no_books)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с книгой из списка книг
@router.callback_query(BookCallbackFactory.filter(F.choose==True))
async def process_book_press(callback: CallbackQuery, callback_data: BookCallbackFactory):
    uid = callback.from_user.id
    db.user_interface.set_current_book(uid, callback_data.book_name)
    db.user_interface.set_current_page(uid, 1)
    page = db.user_interface.get_current_page(uid)
    book = db.user_interface.get_current_book(uid)
    text = db.book_interface.get_page_content(book, page)
    page_num = db.book_interface.get_length(book)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_kb(page, page_num)
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком книг
@router.callback_query(F.data == INLINE_BUTTONS_RU.edit_books)
async def process_books_edit_press(callback: CallbackQuery):
    uid = callback.from_user.id
    books = db.user_interface.get_books(uid)

    await callback.message.edit_text(
        text=ANSWERS_RU.books_edit_menu_title,
        reply_markup=create_books_edit_keyboard(*books)
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "Отменить" в меню редактирования списка книг
@router.callback_query(F.data == INLINE_BUTTONS_RU.edit_books_cancel)
async def process_edit_books_cancel(callback: CallbackQuery):
    uid = callback.from_user.id
    books = db.user_interface.get_books(uid)

    if books:
        await callback.message.edit_text(
            text=ANSWERS_RU.books_menu_title,
            reply_markup=create_books_keyboard(*books)
        )
    else:
        await callback.message.edit_text(text=ANSWERS_RU.no_books)

    await callback.answer()


# Этот хэндлер будет срабатывать если пользователь отправит в чат файл
@router.message(F.document)
async def process_load_book(message: Message):
    await save_users_id(message)

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
        await message.answer(f'Неизвестный формат файла, нужен формат txt')
