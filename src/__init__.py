import os
from flask import Flask
from dotenv import load_dotenv
from backend.src.database.config import db_init
from backend.config import db, ma, migrate, init_env_vars
from backend.src.routes.book_routes import books_blueprint


def create_app():
    load_dotenv()
    env_vars = init_env_vars("LOCAL")
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = env_vars.get("database_uri_full")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.register_blueprint(books_blueprint)
    db_init(env_vars)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app
