from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, CheckConstraint, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Title(Base):
    __tablename__ = 'title'
    TitleID = Column(Integer, primary_key=True)
    title = Column(String(255))

class Category(Base):
    __tablename__ = 'category'
    CategoryID = Column(Integer, primary_key=True)
    category_name = Column(String(255))

class Publisher(Base):
    __tablename__ = 'publisher'
    PublisherID = Column(Integer, primary_key=True)
    publisher_name = Column(String(255))

class Author(Base):
    __tablename__ = 'author'
    AuthorID = Column(Integer, primary_key=True)
    author_last = Column(String(50))
    author_first = Column(String(50))
    author_birth = Column(Integer, CheckConstraint('author_birth BETWEEN -3000 AND EXTRACT(YEAR FROM CURRENT_DATE)'))

class Book(Base):
    __tablename__ = 'book'
    BookID = Column(Integer, primary_key=True)
    AuthorID = Column(Integer, ForeignKey('author.AuthorID'))
    publication_year = Column(Integer)
    PublisherID = Column(Integer, ForeignKey('publisher.PublisherID'))
    TitleID = Column(Integer, ForeignKey('title.TitleID'))
    is_fiction = Column(Boolean)

    author = relationship('Author')
    publisher = relationship('Publisher')
    title = relationship('Title')

class AuthorCategory(Base):
    __tablename__ = 'author_category'
    AuthorCategoryID = Column(Integer, primary_key=True)
    AuthorID = Column(Integer, ForeignKey('author.AuthorID'))
    CategoryID = Column(Integer, ForeignKey('category.CategoryID'))

    author = relationship('Author')
    category = relationship('Category')

class BookCategory(Base):
    __tablename__ = 'book_category'
    BookCategoryID = Column(Integer, primary_key=True)
    BookID = Column(Integer, ForeignKey('book.BookID'))
    CategoryID = Column(Integer, ForeignKey('category.CategoryID'))

    book = relationship('Book')
    category = relationship('Category')

class Patron(Base):
    __tablename__ = 'patron'
    card_number = Column(Integer, primary_key=True)
    patron_last = Column(String(50))
    patron_first = Column(String(50))
    patron_email = Column(String(100))
    join_time = Column(Date, default='CURRENT_DATE')

class Checkout(Base):
    __tablename__ = 'checkout'
    CheckoutID = Column(Integer, primary_key=True)
    card_number = Column(Integer, ForeignKey('patron.card_number'))
    BookID = Column(Integer, ForeignKey('book.BookID'))
    out_date_time = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')
    in_date_time = Column(TIMESTAMP, default='CURRENT_TIMESTAMP + INTERVAL \'7 days\'')
    returned = Column(Boolean)

    patron = relationship('Patron')
    book = relationship('Book')

class Password(Base):
    __tablename__ = 'password'
    PasswordID = Column(Integer, primary_key=True)
    card_number = Column(Integer, ForeignKey('patron.card_number'))
    salt = Column(String(255))
    hash = Column(String(255))

    patron = relationship('Patron')

class PatronCheckout(Base):
    __tablename__ = 'patron_checkout'
    PatronCheckoutID = Column(Integer, primary_key=True)
    card_number = Column(Integer, ForeignKey('patron.card_number'))
    CheckoutID = Column(Integer, ForeignKey('checkout.CheckoutID'))

    patron = relationship('Patron')
    checkout = relationship('Checkout')