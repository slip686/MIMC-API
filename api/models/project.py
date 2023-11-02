from api import db
from api.models.user import UserModel
from sqlalchemy.exc import IntegrityError


class ProjectModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), unique=True)
    picture = db.Column(db.String(255), unique=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id))
    address = db.Column(db.String(255), unique=False)
    time_limits = db.Column(db.String(60), unique=False)
    status = db.Column(db.String(60), unique=False)
    repo_id = db.Column(db.String(255), unique=False)
    users = db.relationship('UsersPartyModel',
                            backref='project_members',
                            lazy='dynamic',
                            cascade="all, delete-orphan")
    docs = db.relationship('DocModel',
                           backref='project_docs',
                           lazy='dynamic',
                           cascade="all, delete-orphan")
    messages = db.relationship('MessageModel',
                               backref='project_messages',
                               lazy='dynamic',
                               cascade="all, delete-orphan")
    structure = db.relationship('DocPlaceModel',
                                backref='project_structure',
                                lazy='dynamic',
                                cascade="all, delete-orphan")
    main_files = db.relationship('MainFileModel',
                                 backref='project_main_files',
                                 lazy='dynamic',
                                 cascade="all, delete-orphan")
    support_files = db.relationship('SupportFileModel',
                                    backref='project_support_files',
                                    lazy='dynamic',
                                    cascade="all, delete-orphan")

    def __init__(self, picture, project_name, owner_id, address, time_limits, status, repo_id):
        self.picture = picture
        self.project_name = project_name
        self.owner_id = owner_id
        self.address = address
        self.time_limits = time_limits
        self.status = status
        self.repo_id = repo_id

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError
