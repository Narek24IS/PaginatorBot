from aiogram.filters.callback_data import CallbackData


class BookCallbackFactory(CallbackData, prefix='%book%'):
    book_name: str
    delete: bool = False
    choose: bool = False

class BookmarksCallbackFactory(CallbackData, prefix='%bookmark%'):
    book_name: str
    page_num: int
    delete: bool = False
    choose: bool = False