from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from lexicon.lexicon import INLINE_BUTTONS_RU


class Keyboard:
    def __init__(self, *buttons: str | KeyboardButton, resize_keyboard: bool = True,
                 is_persistent: bool = False, one_time_keyboard: bool = False):
        self.buttons:list[KeyboardButton] = []
        for button in buttons:
            if isinstance(button, str):
                self.buttons.append(KeyboardButton(text=f'{button}'))
            else:
                self.buttons.append(button)
        self.resize_keyboard = resize_keyboard
        self.is_persistent = is_persistent
        self.one_time_keyboard = one_time_keyboard

    def __call__(self, width: int) -> ReplyKeyboardMarkup:
        kb_builder = ReplyKeyboardBuilder()
        kb_builder.row(*self.buttons, width=width)
        keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(resize_keyboard=self.resize_keyboard,
                                                               is_persistent=self.is_persistent,
                                                               one_time_keyboard=self.one_time_keyboard)
        return keyboard

class InlineKeyboard:
    def __init__(self, *buttons: str|InlineKeyboardButton, last_row:list[InlineKeyboardButton]=[],
                 **data_text: str):
        self.buttons: list[InlineKeyboardButton] = []
        self.last_row = last_row

        if buttons:
            for button in buttons:
                if isinstance(button, str):
                    self._create_button(button)
                else:
                    self.buttons.append(button)
        if data_text:
            for data, text in data_text.items():
                self._create_button(data, text)


    def _create_button(self, data:str, text:str = ''):
        if not text:
            text = vars(INLINE_BUTTONS_RU).get(data, data)
        self.buttons.append(InlineKeyboardButton(text=text, callback_data=data))

    def __call__(self, width: int) -> InlineKeyboardMarkup:
        kb_builder = InlineKeyboardBuilder()
        kb_builder.row(*self.buttons, width=width)
        if self.last_row:
            kb_builder.row(*self.last_row, width=len(self.last_row))
        keyboard: InlineKeyboardMarkup = kb_builder.as_markup()
        return keyboard
