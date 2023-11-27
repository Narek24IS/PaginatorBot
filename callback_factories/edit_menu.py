from aiogram.filters.callback_data import CallbackData


class BookCF(CallbackData, prefix='%book%'):
    book_name: str
    delete: bool = False
    choose: bool = False

class BookmarksCF(CallbackData, prefix='%bookmark%'):
    book_name: str
    page_num: int
    delete: bool = False
    choose: bool = False

class BookMenuButtonCF(CallbackData, prefix='%bookmenu%'):
    edit: bool = False
    cancel: bool = False

class BookmarkMenuButtonCF(CallbackData, prefix='%bookmarkmenu%'):
    edit: bool = False
    cancel: bool = False