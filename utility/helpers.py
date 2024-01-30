from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
from api import app, db, abort
from api.models.doc_place import DocPlaceModel


@app.errorhandler(404)
def not_found(e):
    response = {'status': 404, 'error': e.description}
    return response, 404


def get_object_or_404(model: db.Model, object_id: int):
    model_instance = model.query.get(object_id)
    if model_instance is None:
        abort(404, description=f"{model.__name__.removesuffix('Model')} with id={object_id} not found")
    return model_instance


def flush_place_data(array, db: SQLAlchemy, parent: DocPlaceModel):
    if isinstance(array, list):
        for i in range(len(array)):
            flush_place_data(array=array[i], db=db, parent=parent)
    if isinstance(array, dict):
        for key in array.keys():
            root = flush_single_place(data=array, key=key, db=db)
            root.parent_place_id = parent.place_id
            db.session.flush()
            db.session.refresh(root)
            root.parent_place_id = parent.place_id
            db.session.flush()
            return flush_place_data(array=array.get(key)[1:], db=db, parent=root)


def flush_single_place(data: dict, key: str, db: SQLAlchemy) -> DocPlaceModel:
    root = DocPlaceModel(**data.get(key)[0].get('folder_data'))
    db.session.add(root)
    db.session.flush()
    db.session.refresh(root)
    return root


def generate_key(email):
    cipher_key = Fernet.generate_key()
    cipher = Fernet(cipher_key)
    text = email.encode('UTF-8')
    encrypted_text = cipher.encrypt(text)
    return encrypted_text.decode('UTF-8')
