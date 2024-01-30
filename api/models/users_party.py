from sqlalchemy.exc import IntegrityError

from api import db, Config
from api.models.user import UserModel
from api.models.project import ProjectModel


class UsersPartyModel(db.Model):
    __tablename__ = 'users_party_model'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id))
    project_id = db.Column(db.Integer, db.ForeignKey(ProjectModel.id))
    job_title = db.Column(db.String(255), unique=False)

    def __init__(self, project_id, user_id, job_title):
        self.user_id = user_id
        self.project_id = project_id
        self.job_title = job_title

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError

