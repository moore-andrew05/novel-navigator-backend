import json
from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException
from backend.src import create_app
from backend.src.interfaces.book_response import BookResponse

app = create_app()
app.app_context().push()


@app.errorhandler(404)
def handle_not_found_error(error):
    return BookResponse(False, "Request not found", None).to_json()


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return BookResponse(False, response, None).to_json()


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return BookResponse(False, jsonify(error.messages), None).to_json()


if __name__ == "__main__":
    app.run(debug=True, port=5005, host="0.0.0.0")
