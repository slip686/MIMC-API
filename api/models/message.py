from sqlalchemy.exc import IntegrityError

from api import db, Config
from api.models.user import UserModel
from api.models.project import ProjectModel
from api.models.doc import DocModel
from sqlalchemy import false


class MessageModel(db.Model):
    __tablename__ = 'message_model'
    ntfcn_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(ProjectModel.id))
    doc_id = db.Column(db.Integer, db.ForeignKey(DocModel.doc_id))
    sender_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id))
    receiver_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id))
    receiver_channel = db.Column(db.String(255), unique=False)
    type = db.Column(db.String(255), unique=False)
    comments = db.Column(db.String(511), unique=False)
    time_send = db.Column(db.DateTime, unique=False)
    time_limit = db.Column(db.DateTime, unique=False)
    receive_status = db.Column(db.Boolean, unique=False, default=false(), server_default=false())
    read_status = db.Column(db.Boolean, unique=False, default=false(), server_default=false())
    text = db.Column(db.String(511), unique=False)
    doc_type = db.Column(db.String(60), unique=False)
    place_id = db.Column(db.String(511), unique=False)

    def __init__(self, receiver_id, project_id, doc_id, sender_id, ntfcn_type, comments, time_send, time_limit,
                 msg_text, doc_type, place_id, receiver_channel):
        self.receiver_id = receiver_id
        self.project_id = project_id
        self.doc_id = doc_id
        self.sender_id = sender_id
        self.type = ntfcn_type
        self.comments = comments
        self.time_send = time_send
        self.time_limit = time_limit
        self.text = msg_text
        self.doc_type = doc_type
        self.place_id = place_id
        self.receiver_channel = receiver_channel

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError
