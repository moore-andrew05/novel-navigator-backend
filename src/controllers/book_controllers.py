from flask import request
from backend.config import db
from backend.src.models.library_models import (
    Title,
    Category,
    Publisher,
    Author,
    Book,
    AuthorCategory,
    BookCategory,
    Patron,
    Checkout,
    Password,
    title_schema,
    titles_schema,
    category_schema,
    categories_schema,
    publisher_schema,
    publishers_schema,
    author_schema,
    authors_schema,
    book_schema,
    books_schema,
    author_category_schema,
    author_categories_schema,
    book_category_schema,
    book_categories_schema,
    patron_schema,
    patrons_schema,
    checkout_schema,
    checkouts_schema,
    password_schema,
    passwords_schema,
)
from backend.src.interfaces.book_response import BookResponse

invalid_request = BookResponse(False, "Invalid request", None).to_json()


async def get_books():
    try:
        books = Book.query.all()
        json_books = books_schema.dump(books)
        return BookResponse(True, "Get all books", json_books).to_list()
    except Exception as ex:
        return invalid_request


async def get_book(book_id: int):
    try:
        book = Book.query.get(book_id)

        if book is None:
            return invalid_request

        json_book = book_schema(book)
        return BookResponse(True, "Get book", json_book).to_json()
    except Exception as ex:
        return invalid_request


async def create_book():
    try:
        db.session.autoflush = False
        body = request.json

        if body is None:
            return invalid_request

        # Extract Parameters from request
        title: str = body.get("title")
        author_first: str = body.get("author_first")
        author_last: str = body.get("author_last")
        author_birth: int = body.get("author_birth")
        publisher_name: str = body.get("publisher_name")
        publication_year: int = body.get("publication_year")
        categories: list[str] = body.get("categories")

        # Required Parameters
        if None in (
            title,
            author_first,
            author_last,
            publisher_name,
            publication_year,
        ):
            return invalid_request

        # Need to find ids for foreign keys
        title_id: int
        author_id: int
        publisher_id: int

        # Title ID
        found_title = Title.query.filter(Title.title == title).first()

        if found_title:
            title_id = found_title.title_id

        else:
            found_title = Title(title=title)
            db.session.add(found_title)
            db.session.flush()
            title_id = found_title.title_id

        # Author ID
        if author_birth:
            found_author = Author.query.filter(
                Author.author_last == author_last,
                Author.author_first == author_first,
                Author.author_birth == author_birth,
            ).first()
        else:
            found_author = Author.query.filter(
                Author.author_last == author_last, Author.author_first == author_first
            ).first()

        if found_author:
            author_id = found_author.author_id

        else:
            found_author = Author(
                author_last=author_last,
                author_first=author_first,
                author_birth=author_birth,
            )
            db.session.add(found_author)
            db.session.flush()
            author_id = found_author.author_id

        # Publisher ID
        found_publisher = Publisher.query.filter(
            Publisher.publisher_name == publisher_name
        ).first()

        print(found_publisher)

        if found_publisher:
            publisher_id = found_publisher.publisher_id

        else:
            found_publisher = Publisher(publisher_name=publisher_name)
            db.session.add(found_publisher)
            db.session.flush()
            publisher_id = found_publisher.publisher_id

        book_id: int

        # Create Book to get its ID
        book = Book(
            author_id=author_id,
            publication_year=publication_year,
            publisher_id=publisher_id,
            title_id=title_id,
            returned=True,
        )

        db.session.add(book)
        db.session.flush()
        book_id = book.book_id

        category_ids = []
        new_categories = []

        for category in categories:
            found_category = Category.query.filter(
                Category.category_name == category
            ).first()

            if found_category:
                category_ids.append(found_category.category_id)

            else:
                found_category = Category(category_name=category)
                new_categories.append(found_category)
                db.session.add(found_category)

        db.session.flush()

        for category in new_categories:
            category_ids.append(category.category_id)

        for category_id in category_ids:
            author_category = AuthorCategory(
                author_id=author_id, category_id=category_id
            )
            book_category = BookCategory(book_id=book_id, category_id=category_id)

            db.session.add(author_category)
            db.session.add(book_category)

        db.session.commit()
        json_book = book_schema(book)
        return BookResponse(True, f"Created book with id {book_id}", json_book)

    except Exception as ex:
        db.session.rollback()
        return BookResponse(False, f"{ex}", None).to_json()


# async def create_todo():
#     try:
#         body = request.json

#         if body is None:
#             return invalid_request

#         name = body.get("name")
#         status = body.get("status")

#         if name is None or status is None:
#             return invalid_request

#         todo_id = uuid4()
#         new_todo = Todo(id=todo_id, name=name, status=status)
#         json_todo = todo_schema.dump(new_todo)
#         db.session.add(new_todo)
#         db.session.commit()
#         return TodoResponse(True, "Created a todo", json_todo).to_json()
#     except Exception as ex:
#         print(ex)
#         return invalid_request


# async def update_todo(todo_id):
#     try:
#         todo = Todo.query.get(todo_id)

#         if todo is None:
#             return invalid_request

#         name = request.json.get("name")
#         status = request.json.get("status")

#         if name is None or status is None:
#             return invalid_request

#         todo.name = name
#         todo.status = status
#         json_todo = todo_schema.dump(todo)
#         db.session.add(todo)
#         db.session.commit()
#         return TodoResponse(True, "Updated a todo", json_todo).to_json()
#     except Exception as ex:
#         return invalid_request


# async def remove_todo(todo_id):
#     try:
#         todo = Todo.query.get(todo_id)

#         if todo is None:
#             return invalid_request

#         removed_todo = todo_schema.dump(todo)
#         db.session.delete(todo)
#         db.session.commit()
#         return TodoResponse(True, "Removed a todo", removed_todo).to_json()
#     except Exception as ex:
#         return invalid_request
