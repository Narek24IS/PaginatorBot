from aiogram import Router, F
from aiogram.types import CallbackQuery

from filtres.filtres import IsBookmarkCallbackData, IsDigitCallbackData, IsDelBookmarkCallbackData
from keyboards.keyboards import (create_pagination_kb,
                                 create_bookmarks_keyboard,
                                 create_bookmarks_edit_keyboard)
from lexicon.lexicon import COMMANDS_RU, ANSWERS_RU, INLINE_BUTTONS_RU
from services.database.db_connection import bot_database as db
from callback_factories.edit_menu import BookmarksCallbackFactory

router = Router()


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
@router.callback_query(BookmarksCallbackFactory.filter(F.choose==True))
async def process_bookmark_press(callback: CallbackQuery, callback_data: BookmarksCallbackFactory):
    uid = callback.from_user.id
    book = callback_data.book_name
    page_num = callback_data.page_num
    total_pages = db.book_interface.get_length(book)
    text = db.book_interface.get_page_content(book, page_num)
    db.user_interface.set_current_page(uid, page_num)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_kb(page_num, total_pages)
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@router.callback_query(BookmarksCallbackFactory.filter(F.delete==True))
async def process_del_bookmark_press(callback: CallbackQuery, callback_data: BookmarksCallbackFactory):
    uid = callback.from_user.id
    book = callback_data.book_name
    page_num = callback_data.page_num
    db.user_interface.remove_book_mark(uid, book, page_num)
    bookmarks = db.user_interface.get_book_marks(uid)

    if bookmarks:
        await callback.message.edit_text(
            text=ANSWERS_RU.bookmarks_edit_menu_title,
            reply_markup=create_bookmarks_edit_keyboard(bookmarks)
        )
    else:
        await callback.message.edit_text(text=ANSWERS_RU.no_bookmarks)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(F.data == INLINE_BUTTONS_RU.edit_bookmarks)
async def process_bookmarks_edit_press(callback: CallbackQuery):
    uid = callback.from_user.id
    bookmarks = db.user_interface.get_book_marks(uid)

    await callback.message.edit_text(
        text=ANSWERS_RU.bookmarks_edit_menu_title,
        reply_markup=create_bookmarks_edit_keyboard(bookmarks)
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "Отменить" в меню редактирования списка закладок
@router.callback_query(F.data == INLINE_BUTTONS_RU.edit_bookmarks_cancel)
async def process_bookmarks_edit_press(callback: CallbackQuery):
    uid = callback.from_user.id
    bookmarks = db.user_interface.get_book_marks(uid)

    await callback.message.edit_text(
        text=ANSWERS_RU.bookmarks_menu_title,
        reply_markup=create_bookmarks_keyboard(bookmarks)
    )
    await callback.answer()
