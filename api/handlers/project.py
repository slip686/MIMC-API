from sqlalchemy import text
from api import app, db, multi_auth
from flask import request, abort
from api.models.project import ProjectModel
from api.models.users_party import UsersPartyModel
from api.models.user import UserModel
from utility.helpers import get_object_or_404
from api.schemas.project import projects_schema, project_schema


@app.route("/projects/name/<string:name>")
@multi_auth.login_required
def check_project_existence(name):
    project = ProjectModel.query.filter_by(project_name=name).first()
    if project:
        return project.project_name, 200
    return {'message': 'project name not found'}, 404


@app.route("/projects", methods=["POST"])
@multi_auth.login_required
def add_new_project():
    data = request.json
    new_project = ProjectModel(**data.get('project_data'))
    new_project.save()
    new_project_id = new_project.id
    users = data.get('users')
    for user in users:
        db.session.add(UsersPartyModel(project_id=new_project_id,
                                       user_id=users.get(user).get('user_id'),
                                       job_title=users.get(user).get("job_title")))
    db.session.commit()
    return {"id": new_project.id}, 200


@app.route("/projects/<int:project_id>")
@multi_auth.login_required
def get_project_info(project_id):
    project = get_object_or_404(ProjectModel, project_id)
    return project_schema.dump(project), 200


@app.route('/projects/<int:project_id>/users')
@multi_auth.login_required
def get_project_users(project_id):
    get_object_or_404(ProjectModel, project_id)
    results = db.session.query(UserModel, UsersPartyModel). \
        select_from(UserModel).join(UsersPartyModel).filter_by(project_id=project_id).all()
    results_list = []
    for result in results:
        results_list.append(result[0].as_dict | result[1].as_dict)
    return results_list, 200


@app.route("/projects/<int:project_id>/doc_structure/<string:doctype>")
@multi_auth.login_required
def get_project_doctype_structure(project_id, doctype):
    expression = text(f"SELECT * FROM doc_place_model WHERE project_id = {project_id} AND doc_type = '{doctype}'")
    result = db.session.execute(expression).fetchall()
    if result:
        return [tuple(row) for row in result], 200
    abort(404)
