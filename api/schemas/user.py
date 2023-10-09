from api import ma
from api.models.user import UserModel


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel


class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    email = ma.Str(required=True)
    password = ma.Str(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
