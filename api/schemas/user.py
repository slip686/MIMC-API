from api import ma
from api.models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        exclude = ('password_hash', 'created_on', 'updated_on')


class UserRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

    email = ma.Str(required=True)
    password = ma.Str(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
