import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db: SQLAlchemy = SQLAlchemy()
ma: Marshmallow = Marshmallow()
migrate: Migrate = Migrate()

def init_env_vars(state):
    load_dotenv()
    if state == "LOCAL":
        return {
            "database_uri_full": os.environ.get("DATABASE_URL_LOCAL_FULL"),
            "database_uri": os.environ.get("DATABASE_URL_LOCAL")
        }

    else:
        return {
            "database_uri_full": os.environ.get("DATABASE_URL_FULL"),
            "database_uri": os.environ.get("DATABASE_URL")
        }
