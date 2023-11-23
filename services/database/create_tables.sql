-- drop table if exists users;
-- drop table if exists books;

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
