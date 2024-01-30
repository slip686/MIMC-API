from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from config import Config
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


# def create_app():
#     application = Flask(__name__)
#     application.config.from_object(Config)
#     return application


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)
ctx = app.app_context()
ctx.push()


from api.models.user import UserModel
from api.models.doc import DocModel
from api.models.users_party import UsersPartyModel
from api.models.support_file import SupportFileModel
from api.models.project import ProjectModel
from api.models.message import MessageModel
from api.models.main_file import MainFileModel
from api.models.doc_place import DocPlaceModel
from api.models.doc_place import DocPlaceModel
from api.models.validation_key import ValidationKeyModel


@basic_auth.verify_password
def verify_password(email, password):
    from api.models.user import UserModel
    user = UserModel.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return False
    user.get_stash_user_token(password)
    return user


@token_auth.verify_token
def verify_token(token):
    from api.models.user import UserModel
    user = UserModel.verify_auth_token(token)
    return user
