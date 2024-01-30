import os


class Config:
    DATABASE_URI_DOCKER = os.environ.get('DATABASE_URI_DOCKER',
                                         '')
    DATABASE_URI_HTTP = os.environ.get('DATABASE_URI_REMOTE',
                                       '')
    SQLALCHEMY_DATABASE_URI = DATABASE_URI_HTTP
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True, 'pool_recycle': 300}
    STASH_URL = ''
    STASH_TOKEN = ''
    MSG_BROKER_URL = ''
    MSG_BROKER_LOGIN = ''
    MSG_BROKER_PASS = ''
    SMTP_SOCKET = ''
    SMTP_SERVER_LOGIN = ''
    SMTP_SERVER_PASS = ''
    DEBUG = True
    PORT = 5000
    SECRET_KEY = "PuPa AnD LuPa"
    RESTFUL_JSON = {'ensure_ascii': False}
    SQLALCHEMY_TRACK_MODIFICATIONS = False