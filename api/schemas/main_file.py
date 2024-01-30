from api import ma
from api.models.main_file import MainFileModel


class MainFileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MainFileModel
        fields = ('file_id', 'file_path', 'file_name', 'rev_num',
                  'ver_num', 'document_status', 'status_time_set',
                  'status_time_delta', 'loading_time', 'user_id',
                  'doc_id', 'project_id')


# Десериализация запроса(request)
class MainFileRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = MainFileModel

    # username = ma.Str(required=True)
    # password = ma.Str()
    # role = ma.Str()


main_file_schema = MainFileSchema
main_files_schema = MainFileSchema(many=True)