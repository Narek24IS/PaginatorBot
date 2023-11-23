from services.database.db_connection import bot_database as db

del_query='''
drop table if exists users;
drop table if exists books;
'''

create_query='''
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
);
'''

def setup_db(new:bool=False):
    if new:
        db.execute_query_and_commit(del_query)
    db.execute_query_and_commit(create_query)