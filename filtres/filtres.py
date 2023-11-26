from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('del') and callback.data[:-3].isdigit()

class IsBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return ('/' in callback.data) and (callback.data.replace('/', '').isdigit())

class IsDelBookCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        if callback.data.endswith('del') and '#$%book#$%' in callback.data:
            book_name = callback.data[:-13]
            return {'del_book': book_name}
        return False


class IsBookCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> dict[str, str] | bool:
        if isinstance(callback.data, str) and '#$%book#$%' in callback.data:
            book_name = callback.data[:-10]
            return {'user_book': book_name}
        return False
