from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from lexicon.lexicon import INLINE_BUTTONS_RU
from keyboards.keyboard_builders import InlineKeyboard
from services.file_handling import Book

def new_pagination_kb(page_number, total_pages) -> InlineKeyboardMarkup:
    return InlineKeyboard(INLINE_BUTTONS_RU.backward,
                          f'{page_number}/{total_pages}',
                          INLINE_BUTTONS_RU.forward)(3)


def create_bookmarks_keyboard(book:Book, *args: int) -> InlineKeyboardMarkup:
    # Создаем список кнопок
    buttons:list[InlineKeyboardButton] = []
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for button in sorted(args):
        buttons.append(InlineKeyboardButton(
            text=f'{button} - {book[button][:100]}',
            callback_data=str(button)
        ))
    # Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
    last_row = [
        InlineKeyboardButton(
            text=INLINE_BUTTONS_RU.edit_bookmarks,
            callback_data=INLINE_BUTTONS_RU.edit_bookmarks
        ),
        InlineKeyboardButton(
            text=INLINE_BUTTONS_RU.cancel,
            callback_data=INLINE_BUTTONS_RU.cancel
        )]
    return InlineKeyboard(*buttons, last_row=last_row)(1)


def create_edit_keyboard(book:Book, *args: int) -> InlineKeyboardMarkup:
    # Создаем список кнопок
    buttons:list[InlineKeyboardButton] = []
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for button in sorted(args):
        buttons.append(InlineKeyboardButton(
            text=f'{INLINE_BUTTONS_RU.del_} {button} - {book[button][:100]}',
            callback_data=f'{button}del'
        ))
    # Добавляем в конец клавиатуры кнопку "Отменить"
    last_row = [
        InlineKeyboardButton(
            text=INLINE_BUTTONS_RU.cancel,
            callback_data=INLINE_BUTTONS_RU.cancel
        )]

    return InlineKeyboard(*buttons, last_row=last_row)(1)