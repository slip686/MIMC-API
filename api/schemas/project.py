from api import ma
from api.models.project import ProjectModel


class ProjectSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProjectModel
        fields = ('id', 'project_name', 'picture', 'owner_id', 'address', 'time_limits', 'status', 'repo_id')


# Десериализация запроса(request)
class ProjectRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProjectModel

    # username = ma.Str(required=True)
    # password = ma.Str()
    # role = ma.Str()


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)