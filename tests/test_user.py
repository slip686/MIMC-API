from tests.init_test import client, application, user1, user2, user3, user4, auth_headers_user1, project1


def test_check_email_exists(client, user1):
    headers = {'Content-Type': 'application/json'}
    response = client.get(f'/users/exists', headers=headers, json={"email": "user1@yandex.ru"})
    assert response.status_code == 200


def test_check_email_not_exists(client):
    headers = {'Content-Type': 'application/json'}
    response = client.get(f'/users/exists', headers=headers, json={"email": "user5@yandex.ru"})
    assert response.status_code == 404


def test_check_email_bad_request(client):
    headers = {'Content-Type': 'application/json'}
    response = client.get(f'/users/exists', headers=headers, json={"email": ""})
    assert response.status_code == 400


def test_register_user(client):
    headers = {'Content-Type': 'application/json'}
    user_data = {'email': 'user5@yandex.ru',
                 'first_name': 'Polygraph',
                 'last_name': 'Sharikov',
                 'company_name': 'OOO Panki',
                 'tin': '666',
                 'password': 'qwe321qwe'}
    response = client.post(f'/users/register', headers=headers, json=user_data)
    assert response.status_code == 200


def test_register_user_bad_request(client):
    headers = {'Content-Type': 'application/json'}
    user_data = {'email': 'user6@yandex.ru',
                 'first_name': 'Polygraph',
                 'last_name': 'Sharikov',
                 'company_name': 'OOO Panki',
                 'tin': '666',
                 'password': ''}
    response = client.post(f'/users/register', headers=headers, json=user_data)
    assert response.status_code == 400


def test_restore_pass(client, user1):
    headers = {'Content-Type': 'application/json'}
    credentials = {'email': 'user1@yandex.ru',
                   'password': '123456'}
    response = client.put(f'/users/restore', headers=headers, json=credentials)
    assert response.status_code == 200


def test_restore_pass_bad_request(client):
    headers = {'Content-Type': 'application/json'}
    credentials = {'email': 'user6@yandex.ru',
                   'password': ''}
    response = client.put(f'/users/restore', headers=headers, json=credentials)
    assert response.status_code == 400


def test_get_user_info_by_email(client, user1):
    response = client.get(f'/users/email/user1@yandex.ru')
    assert response.status_code == 200


def test_get_company_list(client, user1, auth_headers_user1):
    response = client.get(f'/company', headers=auth_headers_user1)
    assert response.status_code == 200


def test_get_users_data(client, user1, auth_headers_user1):
    response = client.get(f'/users', headers=auth_headers_user1)
    assert response.status_code == 200


def test_get_user_info_by_id(client, user1, auth_headers_user1):
    response = client.get(f'/users/id/1', headers=auth_headers_user1)
    assert response.status_code == 200


def test_get_user_info_by_id_not_found(client, user1, auth_headers_user1):
    response = client.get(f'/users/id/7', headers=auth_headers_user1)
    assert response.status_code == 404


def test_get_user_roles(client, project1, user1, user2, user3, user4, auth_headers_user1):
    response = client.get(f'/users/id/1/roles', headers=auth_headers_user1)
    assert response.status_code == 200
