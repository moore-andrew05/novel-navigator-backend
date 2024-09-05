from flask import Blueprint, request
import asyncio
from backend.src.controllers.book_controllers import get_books, create_book

books_blueprint = Blueprint("books", __name__, url_prefix="/api/v1/books")


@books_blueprint.route("/", methods=["GET", "POST"])
def book_root():
    if request.method == "GET":
        return asyncio.run(get_books())
    else:
        return asyncio.run(create_book())


# @todos_blueprint.route("/<uuid:todo_id>", methods=["GET", "PUT", "DELETE"])
# def params_route(todo_id):
#     if request.method == "GET":
#         return asyncio.run(get_todo(todo_id))

#     if request.method == "PUT":
#         return asyncio.run(update_todo(todo_id))

#     if request.method == "DELETE":
#         return asyncio.run(remove_todo(todo_id))
