from werkzeug.datastructures import FileStorage
from config import Config
import requests


def create_project_library(lib_name):
    headers = {'Authorization': f'{Config.STASH_TOKEN}', 'Accept': 'application/json; indent=4'}
    data = {'name': lib_name}
    resp = requests.post(f'{Config.STASH_URL}/api2/repos/', headers=headers, data=data)
    return resp.json().get('repo_id')


def create_folders(repo_id):
    folders = 'ddocs', 'cdocs', 'ipdocs'
    headers = {'Authorization': f'{Config.STASH_TOKEN}', 'Accept': 'application/json; charset=utf-8; indent=4'}
    data = {'operation': 'mkdir'}
    for folder in folders:
        requests.post(f'{Config.STASH_URL}/api2/repos/{repo_id}/dir/?p=/{folder}',
                      headers=headers, data=data)


def create_stash_group(name):
    headers = {
        'Authorization': f'{Config.STASH_TOKEN}',
        'Accept': 'application/json; indent=4',
        'Content-Type': 'application/x-www-form-urlencoded'}
    data = f'group_name={name}&group_owner='
    resp = requests.post(f'{Config.STASH_URL}/api/v2.1/admin/groups/', headers=headers, data=data)
    stash_group_id = resp.json().get("id")
    return stash_group_id


def add_user_to_stash_group(group_id, email):
    headers = {
        'Authorization': f'{Config.STASH_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded'}
    data = f'email={email}'
    requests.post(f'{Config.STASH_URL}/api/v2.1/groups/{group_id}/members/', headers=headers, data=data)


def share_stash_lib_to_group(group_id, repo_id):
    headers = {
        'Authorization': f'{Config.STASH_TOKEN}',
        'Accept': 'application/json; indent=4'}
    data = {'repo_id': repo_id, 'share_type': 'group', 'permission': 'rw', 'share_to': [group_id]}
    requests.post(f'{Config.STASH_URL}/api/v2.1/admin/shares/', headers=headers, data=data)


def post_picture(image_name, image_file: FileStorage, repo_id):
    auth_header = {'Authorization': f'{Config.STASH_TOKEN}'}
    raw_link = requests.get(f'{Config.STASH_URL}/api2/repos/{repo_id}/upload-link/', headers=auth_header)
    link = raw_link.text.strip('"')
    file = {'file': (image_name, image_file.stream.read()), 'parent_dir': (None, '/')}
    requests.post(link, headers=auth_header, files=file)
