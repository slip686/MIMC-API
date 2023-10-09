from flask import request
from api import app, db, multi_auth
from api.models.project import ProjectModel
from api.models.doc import DocModel
from api.models.main_file import MainFileModel
from api.models.support_file import SupportFileModel
from api.schemas.main_file import main_file_schema, main_files_schema
from api.schemas.support_file import support_file_schema, support_files_schema
from api.schemas.doc import doc_schema


@app.route("/add_main_file", methods=['POST'])
@multi_auth.login_required
def add_new_main_file():
    data = request.json
    new_main_file = MainFileModel(**data)
    new_main_file.save()
    return {"new_main_file_id": new_main_file.file_id}, 200


@app.route("/add_support_file", methods=['POST'])
@multi_auth.login_required
def add_new_support_file():
    data = request.json
    new_support_file = SupportFileModel(**data)
    new_support_file.save()
    return {"new_support_file_id": new_support_file.id}, 200


@app.route("/doc_main_files/<int:doc_id>")
@multi_auth.login_required
def get_doc_main_files_info(doc_id):
    doc = DocModel.query.filter_by(doc_id=doc_id).first()
    main_files = doc.main_files
    dicts = []
    for main_file in main_files:
        dicts.append(doc_schema.dump(doc) | main_file_schema.dump(main_file))
    return {"doc_and_main_files": dicts}, 200


@app.route("/support_files/<int:project_id>")
@multi_auth.login_required
def get_support_files_info(project_id):
    project = ProjectModel.query.filter_by(id=project_id).first()
    support_files = project.support_files
    return support_files_schema.dump(support_files), 200
