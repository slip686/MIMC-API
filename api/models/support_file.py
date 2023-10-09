from sqlalchemy.exc import IntegrityError

from api import db, Config
from api.models.user import UserModel
from api.models.project import ProjectModel
from api.models.main_file import MainFileModel


class SupportFileModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), unique=False)
    file_type = db.Column(db.String(60), unique=False)
    loading_time = db.Column(db.DateTime, unique=False)
    main_file_id = db.Column(db.Integer, db.ForeignKey(MainFileModel.file_id))
    project_id = db.Column(db.Integer, db.ForeignKey(ProjectModel.id))

    def __init__(self, file_name, file_type, loading_time, main_file_id, project_id):
        self.file_name = file_name
        self.file_type = file_type
        self.loading_time = loading_time
        self.main_file_id = main_file_id
        self.project_id = project_id

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError
