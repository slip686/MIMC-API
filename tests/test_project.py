from tests.init_test import client, application, user1, user2, user3, user4, auth_headers_user1, project1, project_doc_places


def test_check_project_name_existence(client, project1, user1, user2, user3, user4, auth_headers_user1):
    response = client.get(f'/projects/name/{project1.project_name}', headers=auth_headers_user1)
    assert response.status_code == 200


def test_check_project_name_existence_not_found(client, user1, auth_headers_user1):
    response = client.get(f'/projects/name/some name', headers=auth_headers_user1)
    assert response.status_code == 404


def test_add_new_project(client, user1, user2, user3, user4, auth_headers_user1):
    data = {"project_data":
                {"picture": "poooop",
                 "project_name": "poooop2",
                 "owner_id": user1.user_id,
                 "address": "poooop",
                 "time_limits": "poooop",
                 "status": "poooop",
                 "repo_id": "poooop"},
            "users":
                {
                    "user1":
                        {
                            "user_id": user1.user_id,
                            "job_title": "chief_engineer"
                        },
                    "user2":
                        {
                            "user_id": user2.user_id,
                            "job_title": "contractor"
                        },
                    "user3":
                        {
                            "user_id": user3.user_id,
                            "job_title": "designer"
                        },
                    "user4":
                        {
                            "user_id": user4.user_id,
                            "job_title": "technical_client"
                        }
                }
            }
    headers = {'Content-Type': 'application/json'}
    response = client.post(f'/projects', headers=headers | auth_headers_user1, json=data)
    assert response.status_code == 200


def test_get_project_info(client, project1, user1, user2, user3, user4, auth_headers_user1):
    response = client.get(f'/projects/{project1.id}', headers=auth_headers_user1)
    assert response.status_code == 200


def test_get_project_users(client, project1, user1, user2, user3, user4, auth_headers_user1):
    response = client.get(f'/projects/{project1.id}/users', headers=auth_headers_user1)
    assert response.status_code == 200


def test_get_project_doctype_structure(client, project1, user1, user2, user3, user4, project_doc_places,
                                       auth_headers_user1):
    response = client.get(f'/projects/{project1.id}/doc_structure/design', headers=auth_headers_user1)
    assert response.status_code == 200
