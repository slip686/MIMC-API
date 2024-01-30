from api import db
from sqlalchemy.exc import IntegrityError


class ValidationKeyModel(db.Model):
    __tablename__ = 'validation_key_model'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=False)
    key = db.Column(db.String(255), unique=True)

    def __init__(self, email, key):
        self.email = email
        self.key = key

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError

    def delete(self):
        db.session.delete(self)
        db.session.commit()

