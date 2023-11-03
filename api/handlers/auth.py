import requests
from flask import request

from api import app, multi_auth
from config import Config


@app.route('/auth/token')
@multi_auth.login_required
def get_auth_token():
    user = multi_auth.current_user()
    token = user.generate_auth_token()
    return {'api_token': token, 'stash_token': user.stash_token, 'email': user.email, 'user_id': user.user_id,
            'first_name': user.first_name, 'last_name': user.last_name, 'company_name': user.company_name,
            'tin': user.tin}, 200
