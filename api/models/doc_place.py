from psycopg2 import IntegrityError
from sqlalchemy import and_

from api import db, Config
from api.models.user import UserModel
from api.models.project import ProjectModel


class DocPlaceModel(db.Model):
    __tablename__ = 'doc_place_model'
    place_id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.String(32), unique=False)
    name = db.Column(db.String(255), unique=False)
    project_id = db.Column(db.Integer, db.ForeignKey(ProjectModel.id))
    parent_place_id = db.Column(db.Integer, db.ForeignKey('doc_place_model.place_id'))
    # project = db.relationship('ProjectModel', back_populates='structure')
    parent_places = db.relationship('DocPlaceModel',
                                    remote_side=[place_id],
                                    backref='parents',
                                    single_parent=True,
                                    post_update=True)

    def __init__(self, doc_type, name, project_id, parent_place_id=None):
        self.doc_type = doc_type
        self.project_id = project_id
        self.parent_place_id = parent_place_id
        self.name = name

    def get_children_list(self) -> []:
        beginning_getter = db.session.query(DocPlaceModel). \
            filter(DocPlaceModel.place_id == self.place_id).cte(name='children_for', recursive=True)
        with_recursive = beginning_getter.union_all(
            db.session.query(DocPlaceModel).filter(and_(DocPlaceModel.parent_place_id == beginning_getter.c.place_id,
                                                        DocPlaceModel.place_id != DocPlaceModel.parent_place_id)))
        return db.session.query(with_recursive).all()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError
