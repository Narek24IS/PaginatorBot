from dataclasses import dataclass, field


# ---РЕАЛИЗАЦИЯ КЛАССОВ--- #
@dataclass
class BUTTONS_LEXICON:
    forward: str
    backward: str

    edit_bookmarks: str
    cancel:str
    del_:str


@dataclass
class ANSWER_LEXICON:
    edit_bookmarks: str
    del_: str
    no_bookmarks: str
    cancel_text: str


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

    commands:list[COMMAND]