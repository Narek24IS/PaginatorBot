from dataclasses import dataclass


# ---РЕАЛИЗАЦИЯ КЛАССОВ--- #
@dataclass
class BUTTONS_LEXICON:
    forward: str
    backward: str

    edit_bookmarks: str
    edit_bookmarks_cancel: str
    edit_books: str
    edit_books_cancel: str
    del_: str


@dataclass
class ANSWER_LEXICON:
    bookmarks_menu_title: str
    books_menu_title: str
    bookmarks_edit_menu_title: str
    books_edit_menu_title: str

    no_bookmarks: str
    no_books: str

    cancel_text: str
    book_exist: str


@dataclass
class COMMAND:
    command: str
    description: str
    answer: str = ''


@dataclass
class COMMANDS_LEXICON:
    start: COMMAND
    help: COMMAND
    beginning: COMMAND
    continue_: COMMAND
    bookmarks: COMMAND
    books: COMMAND

    commands: list[COMMAND]
