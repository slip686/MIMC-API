from api import ma
from api.models.main_file import MainFileModel


class MainFileSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MainFileModel


# Десериализация запроса(request)
class MainFileRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MainFileModel

    # username = ma.Str(required=True)
    # password = ma.Str()
    # role = ma.Str()


main_file_schema = MainFileSchema
main_files_schema = MainFileSchema(many=True)