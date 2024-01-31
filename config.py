import os


class Config:
    DATABASE_URI_DOCKER = os.environ.get('DATABASE_URI_DOCKER',
                                         'postgresql://api:ddtlbnt yjdsq@srv-captain--exon-db:5433/exon')
    DATABASE_URI_HTTP = os.environ.get('DATABASE_URI_REMOTE',
                                       'postgresql://api:ddtlbnt yjdsq@exon-db.sliplab.net:5433/exon')
    SQLALCHEMY_DATABASE_URI = DATABASE_URI_HTTP
    # SQLALCHEMY_POOL_RECYCLE = 300
    # SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}
    STASH_URL = 'https://cloud.sliplab.net'
    STASH_TOKEN = 'Token 176dee369b20d91944f6a922d2d590ef8143edb7'
    MSG_BROKER_URL = 'messages.sliplab.net'
    MSG_BROKER_LOGIN = 'slip686'
    MSG_BROKER_PASS = 'ddtlbnt yjdsq'
    SMTP_SOCKET = 'smtp.yandex.ru: 587'
    SMTP_SERVER_LOGIN = 'MIMCProjects@yandex.ru'
    SMTP_SERVER_PASS = 'lboxuldvmrxzorna'
    DEBUG = True
    PORT = 5000
    SECRET_KEY = "PuPa AnD LuPa"
    RESTFUL_JSON = {'ensure_ascii': False}
    SQLALCHEMY_TRACK_MODIFICATIONS = False