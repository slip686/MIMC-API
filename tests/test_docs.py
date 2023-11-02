from tests.init_test import client, application, user1, user2, user3, user4, auth_headers_user1, project1, \
    project_doc_places, project_doc1, project_doc2


def test_add_new_doc(client, user1, user2, user3, user4, auth_headers_user1, project1, project_doc_places):
    data = {"project_id": project1.id,
            "document_type": "design",
            "document_cypher": "123",
            "document_name": "PZ",
            "place_id": "1",
            "document_folder": "12345",
            "release_to_work_date": None,
            "start_develop_date": None,
            "end_develop_date": None,
            "document_status": "develop",
            "status_time_set": None}
    headers = {'Content-Type': 'application/json'}
    response = client.post(f'/add_doc', headers=headers | auth_headers_user1, json=data)
    assert response.status_code == 200


def test_get_docs(client, user1, auth_headers_user1, project1, project_doc1, project_doc2):
    response = client.get(f'/get_docs/{project1.id}', headers=auth_headers_user1)
    assert response.status_code == 200


def test_get_doc_by_id(client, user1, auth_headers_user1, project1, project_doc1):
    response = client.get(f'/doc/{project_doc1.doc_id}', headers=auth_headers_user1)
    assert response.status_code == 200


def test_move_doc_to_folder(client, user1, auth_headers_user1, project1, project_doc1, project_doc_places):
    data = {"place_id": 2}
    header = {'Content-Type': 'application/json'}
    response = client.put(f'/docs/{project_doc1.doc_id}/move', headers=header | auth_headers_user1, json=data)
    assert response.status_code == 200
