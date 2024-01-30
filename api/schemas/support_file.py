from api import ma
from api.models.support_file import SupportFileModel


class SupportFileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SupportFileModel
        fields = ('id', 'file_name', 'file_type', 'loading_time', 'main_file_id', 'project_id')


# Десериализация запроса(request)
class SupportFileRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SupportFileModel

    # username = ma.Str(required=True)
    # password = ma.Str()
    # role = ma.Str()


support_file_schema = SupportFileSchema()
support_files_schema = SupportFileSchema(many=True)
