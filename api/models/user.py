from datetime import datetime, timedelta
import requests
import jwt
from api import db, Config
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import URLSafeSerializer, BadSignature
from sqlalchemy.exc import IntegrityError

from api.models.token_blacklist import BlacklistToken


class UserModel(db.Model):
    __tablename__ = 'user_model'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    company_name = db.Column(db.String(255), unique=False)
    notification_table = db.Column(db.String(255), unique=False)
    tin = db.Column(db.String(60), unique=False)
    ntfcn_channel = db.Column(db.String(255), unique=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    projects = db.relationship('UsersPartyModel', backref='users_party_model',
                               cascade="all, delete-orphan",
                               lazy='dynamic')
    main_files = db.relationship('MainFileModel', backref='user_main_files',
                                 cascade="all, delete-orphan",
                                 lazy='dynamic', )
    sent_messages = db.relationship('MessageModel',
                                    backref='as_msg_sender',
                                    primaryjoin="MessageModel.sender_id == UserModel.user_id",
                                    cascade="all, delete-orphan")
    received_messages = db.relationship('MessageModel', lazy='dynamic',
                                        backref='as_msg_receiver',
                                        primaryjoin="MessageModel.receiver_id == UserModel.user_id",
                                        cascade="all, delete-orphan")
    user_own_projects = db.relationship('ProjectModel', lazy='dynamic',
                                        backref='user_own_projects',
                                        primaryjoin="ProjectModel.owner_id == UserModel.user_id",
                                        cascade="all, delete-orphan")

    def __init__(self, email, first_name, last_name, company_name, tin, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.company_name = company_name
        self.tin = tin
        self.ntfcn_channel = email + '_msgchannel'
        self.hash_password(password)
        self.stash_token = None

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, remember=False):
        payload = None
        try:
            if not remember:
                payload = {
                    'exp': datetime.utcnow() + timedelta(days=0, seconds=25),
                    'iat': datetime.utcnow(),
                    'sub': self.user_id}
            else:
                payload = {
                    'exp': datetime.utcnow() + timedelta(days=30),
                    'iat': datetime.utcnow(),
                    'sub': self.user_id}
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def get_id(self):
        return self.user_id

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def verify_auth_token(token):
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        is_blacklisted_token = BlacklistToken.check_blacklist(token)
        if is_blacklisted_token:
            return 'Token blacklisted. Please log in again.'
        else:
            user = UserModel.query.get(payload['sub'])
            return user

    def get_stash_user_token(self, password):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'username={self.email}&password={password}'
        response = requests.post(f'{Config.STASH_URL}/api2/auth-token/', headers=headers, data=data)
        print(response.content)
        self.stash_token = response.json().get('token')


