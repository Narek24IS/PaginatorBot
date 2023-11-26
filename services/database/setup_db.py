from services.book import Book
from services.database.db_connection import bot_database as db

del_query = '''
drop table if exists users;
drop table if exists books;
'''

create_query = '''
CREATE TABLE IF NOT EXISTS books
(
    id serial PRIMARY KEY,
    name text,
    content jsonb
);

CREATE TABLE IF NOT EXISTS users
(
    user_id integer PRIMARY KEY,
    current_book integer,
    current_page integer,
    books integer[],
    book_marks jsonb,
    CONSTRAINT fk_users_current_book FOREIGN KEY (current_book) REFERENCES books (id)
    ON DELETE CASCADE 
    ON UPDATE CASCADE 
);
'''


def get_book_from_file(path: str) -> Book:
    with open(path) as f:
        return Book(text=f.read())

def get_insert_query() -> tuple:
    book1 = get_book_from_file('books/avidreaders.ru__kapitanskaya-dochka.txt')
    book2 = get_book_from_file('books/avidreaders.ru__prestuplenie-i-nakazanie-dr-izd.txt')
    book3 = get_book_from_file('books/avidreaders.ru__puteshestviya-dushi.txt')
    book4 = get_book_from_file('books/avidreaders.ru__sudba-ili-vybor.txt')
    book5 = get_book_from_file('books/Bredberi_Marsianskie-hroniki.txt')

    return (f'''
            INSERT INTO books(name, content)
            VALUES (%s, %s),
            (%s, %s),
            (%s, %s),
            (%s, %s),
            (%s, %s)
            ''', ('Капитанская дочка', book1.get_json_text(),
                  'Преступление и наказание', book2.get_json_text(),
                  'Путешествие души', book3.get_json_text(),
                  'Судьба или выбор', book4.get_json_text(),
                  'Марсианские хроники', book5.get_json_text()))

def setup_db(new: bool = False):
    if new:
        db.execute_query_and_commit(del_query)
        db.execute_query_and_commit(create_query)
        db.execute_query_and_commit(*get_insert_query())
    else:
        db.execute_query_and_commit(create_query)
