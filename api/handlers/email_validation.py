from api import app
from flask import request
from utility.mailer import send_key
from utility.helpers import generate_key
from api.models.user import UserModel
from api.models.validation_key import ValidationKeyModel


@app.route("/get_key", methods=['POST'])
def get_key():
    data = request.json
    email = data.get('email')
    user = UserModel.query.filter_by(email=email).first()
    validation_key = ValidationKeyModel.query.filter_by(email=email).first()
    if user is None or data.get('recover'):
        if validation_key is None:
            key = generate_key(email)
            validation_key = ValidationKeyModel(email=email, key=key)
        else:
            key = generate_key(email)
            validation_key.key = key
        send_result = send_key(email=validation_key.email, key=validation_key.key)
        if send_result == 'success':
            validation_key.save()
            return 'OK', 200
        elif send_result == 'smtp_server_unavailable':
            return 'Server error, try later', 500
        return 'Invalid email', 400
    return 'User exists', 406


@app.route("/accept_key", methods=['POST'])
def accept_key():
    data = request.json
    key = data.get('key')
    validation_key = ValidationKeyModel.query.filter_by(key=key).first()
    if validation_key:
        validation_key.delete()
        return 'OK', 200
    return 'Not found', 404
