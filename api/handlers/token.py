from api import app, multi_auth
from api.models.user import UserModel


@app.route('/auth/token')
@multi_auth.login_required
def get_auth_token():
    email = multi_auth.current_user()
    user = UserModel.query.filter_by(email=email).first()
    token = user.generate_auth_token()
    return {'token': token}
