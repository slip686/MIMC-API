from sqlalchemy.exc import IntegrityError

from api import db, Config
from api.models.user import UserModel
from api.models.project import ProjectModel
from api.models.doc import DocModel


class MainFileModel(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), unique=False)
    file_name = db.Column(db.String(255), unique=False)
    rev_num = db.Column(db.Integer)
    ver_num = db.Column(db.Integer)
    document_status = db.Column(db.String(60), unique=False)
    status_time_set = db.Column(db.DateTime, unique=False)
    status_time_delta = db.Column(db.DateTime, unique=False)
    loading_time = db.Column(db.DateTime, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id))
    doc_id = db.Column(db.Integer, db.ForeignKey(DocModel.doc_id))
    project_id = db.Column(db.Integer, db.ForeignKey(ProjectModel.id))
    support_files = db.relationship('SupportFileModel', backref='support_files', cascade="all, delete-orphan")

    def __init__(self, doc_id, user_id, project_id, name, revision, version,
                 document_status, status_time_set, loading_time):
        self.doc_id = doc_id
        self.user_id = user_id
        self.project_id = project_id
        self.file_name = name
        self.rev_num = revision
        self.ver_num = version
        self.document_status = document_status
        self.status_time_set = status_time_set
        self.loading_time = loading_time

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError
