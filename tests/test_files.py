from tests.init_test import client, application, user1, user2, user3, user4, auth_headers_user1, project1, \
    project_doc_places, project_doc1, project_doc2, main_file1, support_file1


def test_add_new_main_file(client, user1, user2, user3, user4, auth_headers_user1, project1, project_doc_places,
                           project_doc1):
    data = {"doc_id": project_doc1.doc_id,
            "user_id": user1.user_id, "project_id": project1.id,
            "name": "sdfsdf",
            "revision": 1,
            "version": 1,
            "document_status": "just_loaded",
            "status_time_set": None,
            "loading_time": None}
    header = {'Content-Type': 'application/json'}
    response = client.post(f'/add_main_file', headers=header | auth_headers_user1, json=data)
    assert response.status_code == 200


def test_add_new_support_file(client, user1, user2, user3, user4, auth_headers_user1, project1, project_doc_places,
                              project_doc1, main_file1):
    data = {"file_name": 'name',
            "file_type": 'file_type',
            "loading_time": None,
            "main_file_id": main_file1.file_id,
            "project_id": project1.id}
    header = {'Content-Type': 'application/json'}
    response = client.post(f'/add_support_file', headers=header | auth_headers_user1, json=data)
    assert response.status_code == 200


def test_get_doc_main_files_info(client, user1, user2, user3, user4, auth_headers_user1, project1, project_doc_places,
                                 project_doc1, main_file1):
    response = client.get(f'/doc_main_files/{project_doc1.doc_id}', headers=auth_headers_user1)
    assert response.status_code == 200


def test_get_support_files_info(client, user1, user2, user3, user4, auth_headers_user1, project1, project_doc_places,
                                project_doc1, main_file1, support_file1):
    response = client.get(f'/support_files/{project1.id}', headers=auth_headers_user1)
    assert response.status_code == 200
