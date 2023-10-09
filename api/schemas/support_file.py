from api import ma
from api.models.support_file import SupportFileModel


class SupportFileSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SupportFileModel


# Десериализация запроса(request)
class SupportFileRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SupportFileModel

    # username = ma.Str(required=True)
    # password = ma.Str()
    # role = ma.Str()


support_file_schema = SupportFileSchema()
support_files_schema = SupportFileSchema(many=True)
