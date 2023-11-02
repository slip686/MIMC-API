from flask import request
from api import app, db, multi_auth
from api.models.doc import DocModel
from utility.helpers import get_object_or_404
from api.schemas.doc import doc_schema, docs_schema


@app.route("/add_doc", methods=['POST'])
@multi_auth.login_required
def add_new_document():
    data = request.json
    new_doc = DocModel(**data)
    try:
        new_doc.save()
        return {"new_doc_id": new_doc.doc_id}, 200
    except ValueError:
        return "Cypher already exists", 400


@app.route("/get_docs/<int:project_id>")
@multi_auth.login_required
def get_docs(project_id):
    docs = DocModel.query.filter_by(project_id=project_id).all()
    if docs:
        return docs_schema.dump(docs), 200
    return 'Docs not found', 404


@app.route('/doc/<int:doc_id>')
@multi_auth.login_required
def get_doc_by_id(doc_id):
    doc = get_object_or_404(DocModel, doc_id)
    return doc_schema.dump(doc), 200


@app.route('/docs/<int:doc_id>/move', methods=['PUT'])
@multi_auth.login_required
def move_doc_to_folder(doc_id):
    if request.json.get("place_id"):
        doc = get_object_or_404(DocModel, doc_id)
        doc.place_id = request.json.get("place_id")
        db.session.commit()
        return 'Doc moved', 200
