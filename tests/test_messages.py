from tests.init_test import client, application, user1, user2, user3, user4, auth_headers_user1, project1, \
    project_doc_places, project_doc1, project_doc2, main_file1, support_file1, message1, message2


def test_get_messages(client, user1, user2, user3, user4, auth_headers_user1, project1, project_doc_places,
                      project_doc1, message1, message2):
    response = client.get(f'/messages/new/{user1.user_id}', headers=auth_headers_user1)
    assert response.status_code == 200


def test_set_message_received(client, user1, user2, user3, user4, auth_headers_user1, project1, project_doc_places,
                              project_doc1, message1):
    response = client.get(f'/messages/{message1.ntfcn_id}/set_received', headers=auth_headers_user1)
    assert response.status_code == 200


def test_set_message_read(client, user1, user2, user3, user4, auth_headers_user1, project1, project_doc_places,
                          project_doc1, message1):
    response = client.get(f'/messages/{message1.ntfcn_id}/set_read', headers=auth_headers_user1)
    assert response.status_code == 200


def test_send_message(client, user1, user2, user3, user4, auth_headers_user1, project1, project_doc_places,
                      project_doc1, message1):
    data = {"receiver_id": user2.user_id,
            "project_id": project1.id,
            "doc_id": project_doc1.doc_id,
            "sender_id": user1.user_id,
            "ntfcn_type": None,
            "comments": None,
            "time_send": None,
            "time_limit": None,
            "msg_text": None,
            "doc_type": None,
            "place_id": project_doc1.place_id,
            "receiver_channel": user2.ntfcn_channel}
    header = {'Content-Type': 'application/json'}
    response = client.post(f'/messages/new', headers=header | auth_headers_user1, json=data)
    assert response.status_code == 200


def test_get_last_ten_messages(client, user1, user2, user3, user4, auth_headers_user1, project1, project_doc_places,
                               project_doc1, message1, message2):
    offset = 10
    response = client.get(f'/messages/old/{user1.user_id}?offset={offset}', headers=auth_headers_user1)
    assert response.status_code == 200
