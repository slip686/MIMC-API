from api import app, db, Config, multi_auth
from flask import request, abort
from api.models.user import UserModel
from utility.helpers import get_object_or_404
from api.schemas.user import user_schema, users_schema
import requests


@app.route('/users/exists')
def check_email():
    email = request.json.get('email')
    if email:
        user = UserModel.query.filter_by(email=email).first()
        if user:
            return {"status": True}, 200
        return {"status": False}, 404
    return {"status": "no data"}, 400


@app.route('/users/register', methods=['POST'])
def register_user():
    request_data = request.json
    email = request.json.get('email')
    password = request.json.get('password')
    if email and password:
        user = UserModel(**request_data)
        user.save()

        ##############################################################
        # REGISTRATION ON CLOUD FILE STASH
        ##############################################################

        headers = {
            'Authorization': f'{Config.STASH_TOKEN}',
            'Accept': 'application/json; charset=utf-8; indent=4',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = f'email={email}&password={password}'
        requests.post(f'{Config.STASH_URL}/api/v2.1/admin/users/', headers=headers, data=data)

        ##############################################################
        # REGISTRATION ON MESSAGE BROKER
        ##############################################################

        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        data = {"password": "1234", "tags": "management"}
        requests.put(f'http://{Config.MSG_BROKER_URL}/api/users/{email}',
                     auth=(Config.MSG_BROKER_URL, Config.MSG_BROKER_URL),
                     json=data, headers=headers)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        data = {"configure": ".*", "read": ".*", "write": ".*"}
        requests.put(f'http://{Config.MSG_BROKER_URL}/api/permissions/%2F/{email}',
                     auth=(Config.MSG_BROKER_LOGIN, Config.MSG_BROKER_PASS),
                     json=data, headers=headers)

        return {"new_user_id": user.user_id}, 200

    return "Bad request", 400


@app.route('/users/restore', methods=['PUT'])
def restore_pass():
    email = request.json.get('email')
    password = request.json.get('password')
    if email and password:
        user = UserModel.query.filter_by(email=email).first()
        user.hash_password(password)
        db.session.commit()

        ##############################################################
        # RESTORE PASS ON CLOUD FILE STASH
        ##############################################################

        headers = {
            'Authorization': f'{Config.STASH_TOKEN}',
            'Accept': 'application/json; charset=utf-8; indent=4',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {"password": password}
        requests.put(f'{Config.STASH_URL}/api/v2.1/admin/users/{email}/', headers=headers, data=data)

        ##############################################################
        # RESTORE PASS ON MESSAGE BROKER
        ##############################################################

        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        data = {"password": "1234", "tags": "management"}
        requests.put(f'http://{Config.MSG_BROKER_URL}/api/users/{email}',
                     auth=(Config.MSG_BROKER_LOGIN, Config.MSG_BROKER_PASS),
                     json=data, headers=headers)

        return 'Password restored', 200
    return "Bad request", 400


@app.route('/test')
def test():
    return "SERVER IS OK", 200


@app.route('/login_test')
@multi_auth.login_required
def login_test():
    return "LOGGED IN", 202


# @app.route('/login', methods=['POST'])
# def login():
#     email = request.json.get("email")
#     password = request.json.get("password")
#     remember_flag = request.json.get("remember")
#     user = db.session.query(UserModel).filter(UserModel.email == email).first()
#     if user:
#         if user.verify_password(password=password):
#             token = get_stash_user_token(email=email, password=password)
#             if remember_flag:
#                 login_user(user, remember=True)
#                 return user.as_dict | {"stash_token": token}, 202
#             login_user(user)
#             return user_schema.dump(user) | {"stash_token": token}, 202
#         return 'Login unsuccessful', 401
#     return 'Email not found', 404


# @app.route('/logout')
# @multi_auth.login_required
# def logout():
#     logout_user()
#     return "Logged out", 200


@app.route("/users/email/<string:email>")
def get_user_info_by_email(email):
    user = UserModel.query.filter_by(email=email).first()
    if user:
        return user_schema.dump(user), 200
    abort(404)


@app.route("/company")
@multi_auth.login_required
def get_company_list():
    companies = db.session.query(UserModel.company_name).distinct().all()
    company_list = []
    for company_name in companies:
        company_list.append(company_name[0])
    return {"company_list": company_list}, 200


@app.route("/users")
@multi_auth.login_required
def get_users_data():
    users = db.session.query(UserModel).all()
    users_list = users_schema.dump(users)
    return {"users_list": users_list}, 200


@app.route("/users/id/<int:user_id>")
@multi_auth.login_required
def get_user_info_by_id(user_id):
    user = get_object_or_404(UserModel, user_id)
    return user_schema.dump(user), 200


@app.route("/users/id/<int:user_id>/roles")
@multi_auth.login_required
def get_user_roles(user_id):
    user = get_object_or_404(UserModel, user_id)
    roles = user.projects.all()
    roles_dict = {}
    if roles:
        for role in roles:
            roles_dict[role.project_id] = role.job_title
        return roles_dict, 200
    return 'Roles not found', 404
