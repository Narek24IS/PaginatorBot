from lexicon.lexicon_classes import BUTTONS_LEXICON, ANSWER_LEXICON, COMMAND, COMMANDS_LEXICON

# ---СОЗДАНИЕ ЭКЗЕМПЛЯРОВ--- #

ANSWERS_RU = ANSWER_LEXICON(
    edit_bookmarks='<b>Редактировать закладки</b>',
    no_bookmarks='У вас пока нет ни одной закладки.\n\nЧтобы '
                 'добавить страницу в закладки - во время чтения '
                 'книги нажмите на кнопку с номером этой '
                 'страницы\n\n/continue - продолжить чтение',
    cancel_text='/continue - продолжить чтение'
)

INLINE_BUTTONS_RU = BUTTONS_LEXICON(
    forward='>>',
    backward='<<',
    edit_bookmarks='❌ РЕДАКТИРОВАТЬ',
    cancel='ОТМЕНИТЬ',
    del_='❌'
)

start_command = COMMAND(
    command='start',
    description='Запустить бота',
    answer='<b>Привет, читатель!</b>\n\nЭто бот, в котором '
           'ты можешь прочитать книгу Рэя Брэдбери "Марсианские '
           'хроники"\n\nЧтобы посмотреть список доступных '
           'команд - набери /help',
)

help_command = COMMAND(
    command='help',
    description='Справка по работе бота',
    answer='<b>Это бот-читалка</b>\n\nДоступные команды:\n\n/beginning - '
           'перейти в начало книги\n/continue - продолжить '
           'чтение\n/bookmarks - посмотреть список закладок\n/help - '
           'справка по работе бота\n\nЧтобы сохранить закладку - '
           'нажмите на кнопку с номером страницы\n\n<b>Приятного чтения!</b>',
)

bookmarks_command = COMMAND(
    command='bookmarks',
    description='Мои закладки',
    answer='<b>Это список ваших закладок:</b>',
)

beginning_command = COMMAND(
    command='beginning',
    description='В начало книги',
    answer=''
)

continue_command = COMMAND(
    command='continue',
    description='Продолжить чтение',
    answer=''
)

COMMANDS_RU = COMMANDS_LEXICON(
    start=start_command,
    help=help_command,
    beginning=beginning_command,
    continue_=continue_command,
    bookmarks=bookmarks_command,
    commands=[start_command, help_command, beginning_command, continue_command, bookmarks_command]
)

__all__ = [ANSWERS_RU, INLINE_BUTTONS_RU, COMMANDS_RU]
