from api import db, Config
from api.models.user import UserModel
from api.models.project import ProjectModel


class DocPlaceModel(db.Model):
    place_id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.String(32), unique=False)
    project_id = db.Column(db.Integer, db.ForeignKey(ProjectModel.id))
