-- Storing Books/Authors/Etc.

BEGIN;

CREATE TABLE title (
    TitleID SERIAL PRIMARY KEY,
    title VARCHAR(255)
);

CREATE TABLE category (
    CategoryID SERIAL PRIMARY KEY,
    category_name VARCHAR(255)
);

CREATE TABLE publisher (
    PublisherID SERIAL PRIMARY KEY,
    publisher_name VARCHAR(255)
);

CREATE TABLE author (
    AuthorID SERIAL PRIMARY KEY,
    author_last VARCHAR(50),
    author_first VARCHAR(50),
    author_birth INTEGER CHECK (author_birth BETWEEN -3000 AND EXTRACT(YEAR FROM CURRENT_DATE))
);

CREATE TABLE book (
    BookID SERIAL PRIMARY KEY,
    AuthorID INTEGER REFERENCES author,
    publication_year INTEGER,
    PublisherID INTEGER REFERENCES publisher(PublisherID),
    TitleID INTEGER REFERENCES title(TitleID),
    is_fiction BOOLEAN
);

CREATE TABLE author_category (
    AuthorCategoryID SERIAL PRIMARY KEY,
    AuthorID INTEGER REFERENCES author(AuthorID),
    CategoryID INTEGER REFERENCES category(CategoryID)
);

CREATE TABLE book_category (
    BookCategoryID SERIAL PRIMARY KEY,
    BookID INTEGER REFERENCES book(BookID),
    CategoryID INTEGER REFERENCES category(CategoryID)
);


-- Handling users and checkouts

CREATE TABLE patron (
    card_number SERIAL PRIMARY KEY,
    patron_last VARCHAR(50),
    patron_first VARCHAR(50),
    patron_email VARCHAR(100),
    join_time DATE DEFAULT CURRENT_DATE
);

CREATE TABLE checkout (
    CheckoutID SERIAL PRIMARY KEY,
    card_number INTEGER REFERENCES patron(card_number),
    BookID INTEGER REFERENCES book(BookID),
    out_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    in_date_time TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL '7 days'),
    returned BOOLEAN
);

CREATE TABLE password (
    PasswordID SERIAL PRIMARY KEY,
    card_number INTEGER REFERENCES PATRON(card_number),
    salt VARCHAR(255),
    hash VARCHAR(255)
);

CREATE TABLE patron_checkout (
    PatronCheckoutID SERIAL PRIMARY KEY,
    card_number INTEGER REFERENCES patron(card_number),
    CheckoutID INTEGER REFERENCES checkout(CheckoutID)
);

COMMIT;



