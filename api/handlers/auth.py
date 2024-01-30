import requests
from flask import request

from api import app, multi_auth, db
from api.models.user import UserModel
from api.schemas.user import user_schema
from config import Config


@app.route('/auth/token')
@multi_auth.login_required
def get_auth_token():
    token = None
    user = multi_auth.current_user()
    user_data = user_schema.dump(user)
    if request.args.get('remember'):
        token = user.generate_auth_token(remember=True)
    else:
        token = user.generate_auth_token()
    return {'api_token': token, 'stash_token': user.stash_token} | user_data


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    user = db.session.query(UserModel).filter(UserModel.email == email).first()
    if user:
        if user.verify_password(password=password):
            return 'OK', 200
        return {'message': 'Wrong password'}, 401
    return {'message': 'Email not found'}, 404
