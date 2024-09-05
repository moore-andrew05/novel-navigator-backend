from backend.config import db, ma
from sqlalchemy.sql import func, text

"""
SQLAlchemy Models for Library

"""


class Title(db.Model):
    __tablename__ = "title"
    title_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))

    book = db.relationship("Book")


class Category(db.Model):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), unique=True)

    author_category = db.relationship("AuthorCategory")
    book_category = db.relationship("BookCategory")


class Publisher(db.Model):
    __tablename__ = "publisher"
    publisher_id = db.Column(db.Integer, primary_key=True)
    publisher_name = db.Column(db.String(255))

    book = db.relationship("Book")


class Author(db.Model):
    __tablename__ = "author"
    author_id = db.Column(db.Integer, primary_key=True)
    author_last = db.Column(db.String(100))
    author_first = db.Column(db.String(100))
    author_birth = db.Column(db.Integer, nullable=True)

    books = db.relationship("Book")
    author_categories = db.relationship("AuthorCategory")


class Book(db.Model):
    __tablename__ = "book"
    book_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.author_id"))
    publication_year = db.Column(db.Integer)
    publisher_id = db.Column(db.Integer, db.ForeignKey("publisher.publisher_id"))
    title_id = db.Column(db.Integer, db.ForeignKey("title.title_id"))
    returned = db.Column(db.Boolean)

    book_category = db.relationship("BookCategory")
    checkout = db.relationship("Checkout")


class AuthorCategory(db.Model):
    __tablename__ = "author_category"
    author_category_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.author_id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))


class BookCategory(db.Model):
    __tablename__ = "book_category"
    book_category_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))


"""

"""


"""
SQLAlchemy Models for Patrons

"""


class Patron(db.Model):
    __tablename__ = "patron"
    card_number = db.Column(db.Integer, primary_key=True)
    patron_last = db.Column(db.String(50))
    patron_first = db.Column(db.String(100))
    patron_email = db.Column(db.String(255))
    join_time = db.Column(db.DateTime, server_default=func.current_timestamp())

    checkouts = db.relationship("Checkout")
    password = db.relationship("Password")


class Checkout(db.Model):
    __tablename__ = "checkout"
    checkout_id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.Integer, db.ForeignKey("patron.card_number"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id"))
    out_time = db.Column(db.DateTime, server_default=func.current_timestamp())
    due_time = db.Column(
        db.DateTime, server_default=text("(CURRENT_TIMESTAMP + INTERVAL '21 days')")
    )
    returned = db.Column(db.Boolean, default=False)


class Password(db.Model):
    __tablename__ = "password"
    password_id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.Integer, db.ForeignKey("patron.card_number"))
    salt_val = db.Column(db.String(255))
    hash_val = db.Column(db.String(255))


"""
Marshmallow Schemas for Library

"""


class TitleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Title
        include_relationships = False
        load_instance = True


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_relationships = False
        load_instance = True


class PublisherSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Publisher
        include_relationships = False
        load_instance = True


class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        include_relationships = False
        load_instance = True


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        include_relationships = False
        load_instance = True


class AuthorCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthorCategory
        include_fk = True
        load_instance = True


class BookCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthorCategory
        include_fk = True
        load_instance = True


"""
Marshmallow Schemas for Patrons

"""


class PatronSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patron
        include_relationships = False
        load_instance = True


class CheckoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Checkout
        include_fk = True
        load_instance = True


class PasswordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patron
        include_fk = True
        load_instance = True


"""
Schema Objects
"""

title_schema = TitleSchema()
titles_schema = TitleSchema(many=True)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

publisher_schema = PublisherSchema()
publishers_schema = PublisherSchema(many=True)

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

author_category_schema = AuthorCategorySchema()
author_categories_schema = AuthorCategorySchema(many=True)

book_category_schema = BookCategorySchema()
book_categories_schema = BookCategorySchema(many=True)

patron_schema = PatronSchema()
patrons_schema = PatronSchema(many=True)

checkout_schema = CheckoutSchema()
checkouts_schema = CheckoutSchema(many=True)

password_schema = PasswordSchema()
passwords_schema = PasswordSchema(many=True)
