import pytest
import os

os.environ['DATABASE_URI_REMOTE'] = 'sqlite:///:memory:'
from api import db
from app import app
from base64 import b64encode
from api.models.user import UserModel
from api.models.project import ProjectModel
from api.models.users_party import UsersPartyModel
from api.models.doc import DocModel
from api.models.main_file import MainFileModel
from api.models.support_file import SupportFileModel
from api.models.message import MessageModel


@pytest.fixture()
def application():
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture()
def client(application):
    return application.test_client()


@pytest.fixture()
def user1():
    user_data = {'email': 'user1@yandex.ru',
                 'first_name': 'Pupa',
                 'last_name': 'Zalupkin',
                 'company_name': 'OOO Panki',
                 'tin': '666',
                 'password': 'qwe321qwe'}
    user = UserModel(**user_data)
    user.save()
    return user


@pytest.fixture()
def auth_headers_user1(user1):
    user_data = {'email': 'user1@yandex.ru', 'password': 'qwe321qwe'}
    headers = {
        'Authorization': 'Basic ' + b64encode(
            f"{user_data['email']}:{user_data['password']}".encode('ascii')).decode('utf-8')
    }
    return headers


@pytest.fixture()
def user2():
    user_data = {'email': 'user2@yandex.ru',
                 'first_name': 'Lupa',
                 'last_name': 'Zapupkin',
                 'company_name': 'OOO Panki',
                 'tin': '666',
                 'password': 'qwe321qwe'}
    user = UserModel(**user_data)
    user.save()
    return user


@pytest.fixture()
def auth_headers_user_2(user2):
    user_data = {'email': 'user2@yandex.ru', 'password': 'qwe321qwe'}
    headers = {
        'Authorization': 'Basic ' + b64encode(
            f"{user_data['email']}:{user_data['password']}".encode('ascii')).decode('utf-8')
    }
    return headers


@pytest.fixture()
def user3():
    user_data = {'email': 'user3@yandex.ru',
                 'first_name': 'Biba',
                 'last_name': 'Bobkin',
                 'company_name': 'OOO Panki',
                 'tin': '666',
                 'password': 'qwe321qwe'}
    user = UserModel(**user_data)
    user.save()
    return user


@pytest.fixture()
def auth_headers_user_3(user3):
    user_data = {'email': 'user3@yandex.ru', 'password': 'qwe321qwe'}
    headers = {
        'Authorization': 'Basic ' + b64encode(
            f"{user_data['email']}:{user_data['password']}".encode('ascii')).decode('utf-8')
    }
    return headers


@pytest.fixture()
def user4():
    user_data = {'email': 'user4@yandex.ru',
                 'first_name': 'Boba',
                 'last_name': 'Bibkin',
                 'company_name': 'OOO Panki',
                 'tin': '666',
                 'password': 'qwe321qwe'}
    user = UserModel(**user_data)
    user.save()
    return user


@pytest.fixture()
def auth_headers_user_4(user4):
    user_data = {'email': 'user4@yandex.ru', 'password': 'qwe321qwe'}
    headers = {
        'Authorization': 'Basic ' + b64encode(
            f"{user_data['email']}:{user_data['password']}".encode('ascii')).decode('utf-8')
    }
    return headers


@pytest.fixture()
def user5():
    user_data = {'email': 'user666@yandex.ru',
                 'first_name': 'Boba',
                 'last_name': 'Bibkin',
                 'company_name': 'OOO Panki',
                 'tin': '666',
                 'password': 'qwe321qwe'}
    user = UserModel(**user_data)
    user.save()
    return user


@pytest.fixture()
def auth_headers_user_5(user5):
    user_data = {'email': 'user666@yandex.ru', 'password': 'qwe321qwe'}
    headers = {
        'Authorization': 'Basic ' + b64encode(
            f"{user_data['email']}:{user_data['password']}".encode('ascii')).decode('utf-8')
    }
    return headers


@pytest.fixture()
def project1(client, user1, user2, user3, user4, auth_headers_user1):
    project_data = {"picture": "poooop",
                    "project_name": "poooop",
                    "owner_id": user1.user_id,
                    "address": "poooop",
                    "time_limits": "poooop",
                    "status": "poooop",
                    "repo_id": "poooop"}
    project = ProjectModel(**project_data)
    project_id = project.id
    project.save()
    users_party_data = [{"project_id": project_id,
                         "user_id": user1.user_id,
                         "job_title": "chief_engineer"},
                        {"project_id": project_id,
                         "user_id": user2.user_id,
                         "job_title": "contractor"},
                        {"project_id": project_id,
                         "user_id": user3.user_id,
                         "job_title": "designer"},
                        {"project_id": project_id,
                         "user_id": user4.user_id,
                         "job_title": "technical_client"}]
    for part in users_party_data:
        user_part = UsersPartyModel(**part)
        user_part.save()
    return project


@pytest.fixture()
def project_doc_places(client, project1, user1, auth_headers_user1):
    client.post(f'/add_column_to_structure/1', headers=auth_headers_user1)
    client.post(f'/add_column_to_structure/2', headers=auth_headers_user1)
    data = {"columns": "1, 2", "values": "asdfasdf|ertyrty"}
    header = {'Content-Type': 'application/json'}
    client.post(f'/add_place/{project1.id}/design', headers=header | auth_headers_user1, json=data)
    data = {"columns": "1, 2", "values": "asdfasdf|xvbxcvb"}
    client.post(f'/add_place/{project1.id}/design', headers=header | auth_headers_user1, json=data)


@pytest.fixture()
def project_doc1(client, project1, project_doc_places, user1, auth_headers_user1):
    doc1 = DocModel(project_id=project1.id,
                    document_type='design',
                    document_cypher='123',
                    document_name='456',
                    place_id=1,
                    document_folder='asdfasdf',
                    release_to_work_date=None,
                    start_develop_date=None,
                    end_develop_date=None,
                    document_status='develop',
                    status_time_set=None)
    doc1.save()
    return doc1


@pytest.fixture()
def project_doc2(client, project1, project_doc_places, user1, auth_headers_user1):
    doc2 = DocModel(project_id=project1.id,
                    document_type='design',
                    document_cypher='789',
                    document_name='456',
                    place_id=1,
                    document_folder='asdfasdf',
                    release_to_work_date=None,
                    start_develop_date=None,
                    end_develop_date=None,
                    document_status='develop',
                    status_time_set=None)
    doc2.save()
    return doc2


@pytest.fixture()
def main_file1(client, project1, project_doc1, project_doc_places, user1, auth_headers_user1):
    file1 = MainFileModel(doc_id=project_doc1.doc_id,
                          user_id=user1.user_id,
                          project_id=project1.id,
                          name="main_file1",
                          revision=1,
                          version=1,
                          document_status="just_loaded",
                          status_time_set=None,
                          loading_time=None)
    file1.save()
    return file1


@pytest.fixture()
def support_file1(client, project1, project_doc1, main_file1, project_doc_places, user1, auth_headers_user1):
    support_file = SupportFileModel(file_name='name',
                                    file_type='file_type',
                                    loading_time=None,
                                    main_file_id=main_file1.file_id,
                                    project_id=project1.id)
    support_file.save()
    return support_file


@pytest.fixture()
def message1(client, user1, user2, project1, project_doc1):
    new_message = MessageModel(receiver_id=user1.user_id,
                               project_id=project1.id,
                               doc_id=project_doc1.doc_id,
                               sender_id=user2.user_id,
                               ntfcn_type=None,
                               comments=None,
                               time_send=None,
                               time_limit=None,
                               msg_text=None,
                               doc_type=None,
                               place_id=project_doc1.place_id,
                               receiver_channel=user1.ntfcn_channel)
    new_message.save()
    return new_message


@pytest.fixture()
def message2(client, user1, user2, user3, project1, project_doc1):
    new_message = MessageModel(receiver_id=user1.user_id,
                               project_id=project1.id,
                               doc_id=project_doc1.doc_id,
                               sender_id=user3.user_id,
                               ntfcn_type=None,
                               comments=None,
                               time_send=None,
                               time_limit=None,
                               msg_text=None,
                               doc_type=None,
                               place_id=project_doc1.place_id,
                               receiver_channel=user1.ntfcn_channel)
    new_message.save()
    return new_message
