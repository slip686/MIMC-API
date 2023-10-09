from api import ma
from api.models.project import ProjectModel


class ProjectSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProjectModel


# Десериализация запроса(request)
class ProjectRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProjectModel

    # username = ma.Str(required=True)
    # password = ma.Str()
    # role = ma.Str()


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)