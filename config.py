from dotenv import load_dotenv
load_dotenv()

import os
basedir = os.path.abspath(os.path.dirname(__file__))

print(basedir)

class Config(object):
    DEBUG = False
    DEVELOPMENT = False

    SQLALCHEMY_DATABASE_URI = \
    f'postgresql://{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}'

class ProductionConfig(Config):
    pass

class StagingConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
