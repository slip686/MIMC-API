import json

import sqlalchemy
from psycopg2 import IntegrityError
from sqlalchemy import text, and_
from api import app, db, multi_auth
from api.models.doc_place import DocPlaceModel
from api.models.project import ProjectModel
from api.schemas.doc_place import doc_place_schema, doc_place_schemas
from flask import request, abort, jsonify
from utility.helpers import get_object_or_404, flush_single_place, flush_place_data


@app.route("/place/del/<int:place_id>", methods=['DELETE'])
@multi_auth.login_required
def delete_place(place_id):
    place: DocPlaceModel = get_object_or_404(DocPlaceModel, place_id)
    children: list[sqlalchemy.engine.row.Row] = place.get_children_list()
    if children:
        dicts: list[dict] = doc_place_schemas.dump(children)
        model_objects = doc_place_schemas.load(reversed(dicts))
        for item in model_objects:
            db.session.delete(item)
        db.session.commit()
    return 'OK', 200


@app.route("/place/add", methods=['POST'])
@multi_auth.login_required
def add_place():
    data = request.json

    roots: list[DocPlaceModel] = []
    children: list[DocPlaceModel] = []

    def save(items_list):
        for item in items_list:
            db.session.add(item)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError

    def is_root(item: DocPlaceModel):
        if not item.parent_place_id:
            return True
        return False

    if not isinstance(data, dict):
        for place in data:
            new_place = DocPlaceModel(**place)
            if is_root(new_place):
                roots.append(new_place)
            else:
                children.append(new_place)
    else:
        new_place = DocPlaceModel(**data)
        if is_root(new_place):
            roots.append(new_place)
        else:
            children.append(new_place)

    roots_ids = []
    children_ids = []

    try:
        if roots:
            save(roots)
            for root in roots:
                roots_ids.append(root.place_id)
                root.parent_place_id = root.place_id
            db.session.commit()
        if children:
            save(children)
            for child in children:
                children_ids.append(child.place_id)

        return {'roots_ids': roots_ids, 'children_ids': children_ids}, 200
    except ValueError:
        abort(400)


@app.route("/place/add/bunch", methods=['POST'])
@multi_auth.login_required
def add_place_bunch():
    data = request.json

    for key in data.keys():
        root = flush_single_place(data=data, key=key, db=db)
        parent_id = root.place_id
        root.parent_place_id = parent_id
        db.session.flush()
        flush_place_data(data.get(key)[1:], db=db, parent=root)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

    return {'status': 'OK'}, 200


@app.route("/place/get_structure/<int:project_id>/<string:doctype>")
@multi_auth.login_required
def get_project_doctype_structure(project_id, doctype):
    project: ProjectModel = get_object_or_404(ProjectModel, project_id)
    structure = project.structure.filter(DocPlaceModel.doc_type == doctype)
    if structure:
        return jsonify({'structure': doc_place_schemas.dump(structure)}), 200
    abort(404)


@app.route("/place/rename/<int:place_id>/<string:new_name>", methods=['PUT'])
@multi_auth.login_required
def rename_place(place_id, new_name):
    place: DocPlaceModel = get_object_or_404(DocPlaceModel, place_id)
    old_name = place.name
    place.name = new_name
    db.session.commit()
    return jsonify({'place_id': place.place_id, 'old_name': old_name, 'new_name': place.name}), 200


@app.route("/place/move/<int:place_id>/<int:new_parent_place_id>", methods=['PUT'])
@multi_auth.login_required
def move_place(place_id, new_parent_place_id):
    place: DocPlaceModel = get_object_or_404(DocPlaceModel, place_id)
    old_parent_place_id = place.parent_place_id
    old_parent_place = get_object_or_404(DocPlaceModel, place.parent_place_id)
    old_parent_place_name = old_parent_place.name
    place.parent_place_id = new_parent_place_id
    new_parent_place = get_object_or_404(DocPlaceModel, new_parent_place_id)
    new_parent_place_name = new_parent_place.name
    db.session.commit()
    return jsonify({'place_id': place.place_id, 'old_parent_place_id': old_parent_place_id,
                    'old_parent_place_name': old_parent_place_name,
                    'new_parent_place_id': place.parent_place_id,
                    'new_parent_place_name': new_parent_place_name}), 200
