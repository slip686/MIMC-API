from api import ma
from api.models.doc import DocModel


class DocSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DocModel


# Десериализация запроса(request)
class DocRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DocModel

    # username = ma.Str(required=True)
    # password = ma.Str()
    # role = ma.Str()


doc_schema = DocSchema()
docs_schema = DocSchema(many=True)