from api import ma
from api.models.message import MessageModel


class MessageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MessageModel
        fields = ('ntfcn_id', 'project_id', 'doc_id', 'sender_id',
                  'receiver_id', 'receiver_channel', 'type', 'comments',
                  'time_send', 'time_limit', 'receive_status', 'read_status',
                  'text', 'doc_type', 'place_id')


# Десериализация запроса(request)
class MessageRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MessageModel

    # username = ma.Str(required=True)
    # password = ma.Str()
    # role = ma.Str()


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)