from sqlalchemy.exc import IntegrityError

from api import db, Config
from api.models.user import UserModel
from api.models.project import ProjectModel


class DocModel(db.Model):
    doc_id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(32), unique=False)
    document_name = db.Column(db.String(255), unique=False)
    document_cypher = db.Column(db.String(127), unique=True)
    release_to_work_date = db.Column(db.Date, unique=False)
    start_develop_date = db.Column(db.Date, unique=False)
    end_develop_date = db.Column(db.Date, unique=False)
    document_status = db.Column(db.String(60), unique=False)
    status_time_set = db.Column(db.DateTime, unique=False)
    place_id = db.Column(db.String(255), unique=False)
    document_folder = db.Column(db.String(32), unique=False)
    project_id = db.Column(db.Integer, db.ForeignKey(ProjectModel.id))
    main_files = db.relationship('MainFileModel', backref='doc_main_files', cascade="all, delete-orphan")
    messages = db.relationship('MessageModel', backref='doc_messages', cascade="all, delete-orphan")

    def __init__(self, project_id, document_type, document_cypher, document_name, place_id, document_folder,
                 release_to_work_date, start_develop_date, end_develop_date, document_status, status_time_set):
        self.project_id = project_id
        self.document_type = document_type
        self.document_cypher = document_cypher
        self.document_name = document_name
        self.place_id = place_id
        self.document_folder = document_folder
        self.release_to_work_date = release_to_work_date
        self.start_develop_date = start_develop_date
        self.end_develop_date = end_develop_date
        self.document_status = document_status
        self.status_time_set = status_time_set

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError
