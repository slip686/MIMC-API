from api import ma
from api.models.user import UserModel


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel


class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        exclude = ('password_hash',)

    email = ma.Str(required=True)
    password = ma.Str(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_request_schema = UserRequestSchema()
