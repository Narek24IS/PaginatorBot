from lexicon.lexicon_classes import BUTTONS_LEXICON, ANSWER_LEXICON, COMMAND, COMMANDS_LEXICON

# ---СОЗДАНИЕ ЭКЗЕМПЛЯРОВ--- #

ANSWERS_RU = ANSWER_LEXICON(
    edit_bookmarks='<b>Редактировать закладки</b>',
    no_bookmarks='У вас пока нет ни одной закладки.\n\nЧтобы '
                 'добавить страницу в закладки - во время чтения '
                 'книги нажмите на кнопку с номером этой '
                 'страницы\n\n/continue - продолжить чтение',
    no_books='У вас пока нет ни одной книги.\n\nЧтобы '
             'добавить книги для чтения просто отправьте книгу '
             'в виду текстового файла',
    cancel_text='/continue - продолжить чтение',
    book_exist='Книга с таким именем уже существует, попробуйте переименовать файл'
)

INLINE_BUTTONS_RU = BUTTONS_LEXICON(
    forward='>>',
    backward='<<',
    edit_bookmarks='❌ РЕДАКТИРОВАТЬ',
    edit_bookmarks_cancel='ОТМЕНИТЬ',
    edit_books='❌РЕДАКТИРОВАТЬ',
    edit_books_cancel=' ОТМЕНИТЬ',
    del_='❌'
)

start_command = COMMAND(
    command='start',
    description='Запустить бота',
    answer='<b>Привет, читатель!</b>\n\n'
           'Это бот, в котором ты можешь сохранять и читать книги\n\n'
           'Чтобы посмотреть список доступных команд - набери /help\n\n'
           'Чтобы добавить книгу, отправьте её в виде текстового файла в любой момент нашего '
           'общения, если требуется задать имя отличное от имени файла, отправьте его в поле под файлом.\n\n'
           'Чтобы сохранить закладку - нажмите на кнопку с номером страницы.\n\n'
           'Мы уже добавили несколько книг в твою библиотеку, чтобы ты мог проверить функционал бота\n'
           'Для просмотра списка доступных книг - введи команду /books',
)

help_command = COMMAND(
    command='help',
    description='Справка по работе бота',
    answer='<b>Это бот-читалка</b>\n\nДоступные команды:\n\n/beginning - '
           'перейти в начало книги\n/continue - продолжить '
           'чтение\n/bookmarks - посмотреть список закладок\n/help - '
           'справка по работе бота\n\nЧтобы сохранить закладку - '
           'нажмите на кнопку с номером страницы\n\n'
           'Чтобы добавить книгу, отправьте её в виде текстового файла в любой момент нашего '
           'общения, если требуется задать имя отличное от имени файла, отправьте его в поле под файлом.\n\n'
           '<b>Приятного чтения!</b>',
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

books_command = COMMAND(
    command='books',
    description='Мои книги',
    answer='Посмотреть загруженные книги'
)

COMMANDS_RU = COMMANDS_LEXICON(
    start=start_command,
    help=help_command,
    beginning=beginning_command,
    continue_=continue_command,
    bookmarks=bookmarks_command,
    books=books_command,
    commands=[beginning_command, continue_command, bookmarks_command, books_command, help_command]
)

__all__ = [ANSWERS_RU, INLINE_BUTTONS_RU, COMMANDS_RU]
