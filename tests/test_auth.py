import pytest
from tests.init_test import client, application, user1, user5, auth_headers_user1, auth_headers_user_5
from api.models.user import UserModel


def test_basic_auth(client, auth_headers_user_5, user5):
    response = client.get('/auth/token', headers=auth_headers_user_5)
    data = response.json
    assert response.status_code == 200
    assert data["api_token"] == user5.generate_auth_token()
    # assert data["stash_token"] is not None


def test_token_auth(client, user1):
    token = user1.generate_auth_token()
    headers = {'Authorization': 'Bearer ' + token}
    response = client.get('/login_test', headers=headers)
    assert response.status_code == 202
