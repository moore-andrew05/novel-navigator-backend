# React Backend

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
env_config = os.getenv('APP_SETTINGS', "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from db.models import *

@app.route('/')
def hello_world():
    print("Hello World")


if __name__ == "__main__":
    app.run()

