from api import ma
from api.models.message import MessageModel


class MessageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MessageModel


# Десериализация запроса(request)
class MessageRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MessageModel

    # username = ma.Str(required=True)
    # password = ma.Str()
    # role = ma.Str()


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)