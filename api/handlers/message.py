from api import app, db, multi_auth
from api.models.user import UserModel
from api.models.message import MessageModel
from sqlalchemy import false, and_
from flask import request
from api.helpers import get_object_or_404
from api.schemas.message import messages_schema


@app.route("/messages/new/<int:user_id>")
@multi_auth.login_required
def get_messages(user_id):
    user = get_object_or_404(UserModel, user_id)
    messages = user.received_messages.filter_by(read_status=false()).order_by(MessageModel.ntfcn_id).all()
    if messages:
        return messages_schema.dump(messages), 200
    return "No messages", 404


@app.route('/messages/<int:ntfcn_id>/set_received')
@multi_auth.login_required
def set_message_received(ntfcn_id):
    message = get_object_or_404(MessageModel, ntfcn_id)
    message.receive_status = True
    db.session.commit()
    return 'Receive status sat', 200


@app.route('/messages/<int:ntfcn_id>/set_read')
@multi_auth.login_required
def set_message_read(ntfcn_id):
    message = get_object_or_404(MessageModel, ntfcn_id)
    message.read_status = True
    db.session.commit()
    return 'Read status sat', 200


@app.route('/messages/new', methods=['POST'])
@multi_auth.login_required
def send_message():
    message = MessageModel(**request.json)
    message.save()
    return f'{message.ntfcn_id}', 200


@app.route('/messages/old/<int:user_id>')
@multi_auth.login_required
def get_last_ten_messages(user_id):
    messages = None
    user = get_object_or_404(UserModel, user_id)
    offset = request.args.get('offset')
    if not eval(offset):
        messages = user.received_messages.filter(and_(MessageModel.receive_status,
                                                      MessageModel.read_status)).order_by(
            MessageModel.ntfcn_id.desc()).limit(10)
    else:
        messages = user.received_messages.filter(and_(MessageModel.receive_status,
                                                      MessageModel.read_status)).order_by(
            MessageModel.ntfcn_id.desc()).offset(int(offset)).limit(10)
    if messages:
        return messages_schema.dump(messages)
    return "No messages", 404
