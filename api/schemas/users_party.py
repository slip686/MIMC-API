from api import ma
from api.models.users_party import UsersPartyModel


class UsersPartySchema(ma.SQLAlchemySchema):
    class Meta:
        model = UsersPartyModel


# Десериализация запроса(request)
class UsersPartyRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UsersPartyModel

    # username = ma.Str(required=True)
    # password = ma.Str()
    # role = ma.Str()


users_party_schema = UsersPartySchema()
users_parties_schema = UsersPartySchema(many=True)