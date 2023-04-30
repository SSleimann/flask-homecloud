import os
import io

import typing as t

from ...models import User
from ...utils import get_path_files_and_folders

T = t.TypeVar('T')

def initialize(test_client, user: User, state: t.Literal['private', 'public']) -> T:
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    file = io.BytesIO(b"testing")
    payload_file = {
        'file': (file, 'test.txt'),
        'next': '/main/cloud/{0}'.format(state),
    }
    
    res_file = test_client.post(
        '/main/cloud/upload_file/{0}/usertest/path/'.format(state),
        data=payload_file,
        follow_redirects=True
    )
    
    payload_folder = {
        'next': '/main/cloud/{0}'.format(state),
        'dir': 'testFolder'
    }
    
    res_folder = test_client.post(
        '/main/cloud/create_dir/{0}/usertest/path/'.format(state),
        data=payload_folder,
        follow_redirects=True
    )
    
    return res_file, res_folder

def test_rename_file_private(test_client, user):
    res_file, res_folder = initialize(test_client, user, 'private')
    
    full_path = os.path.join(user.get_private_user_path(), '')
    files, folders = get_path_files_and_folders(full_path)
    file = files[0]
    
    payload = {
        'name': 'juancarlos'
    }
    
    res = test_client.post(
        '/main/cloud/rename/private/usertest/path/{0}/'.format(file.relpath),
        data=payload,
        follow_redirects=True
    )
    
    files_new, folders_new = get_path_files_and_folders(full_path)
    
    assert res.status_code == 200
    assert b'juancarlos' in res.data
    assert file.entry.name != files_new[0].entry.name
    assert files_new[0].entry.name == 'juancarlos'
    assert b'Se ha renombrado con exito!' in res.data
    assert b'Cloud private' in res.data

def test_rename_folder_private(test_client, user):
    res_file, res_folder = initialize(test_client, user, 'private')

    full_path = os.path.join(user.get_private_user_path(), '')
    files, folders = get_path_files_and_folders(full_path)
    folder = folders[0]
    
    payload = {
        'name': 'juancarlosfolder'
    }
    
    res = test_client.post(
        '/main/cloud/rename/private/usertest/path/{0}/'.format(folder.relpath),
        data=payload,
        follow_redirects=True
    )
    
    files_new, folders_new = get_path_files_and_folders(full_path)
    
    assert res.status_code == 200
    assert b'juancarlosfolder' in res.data
    assert folder.entry.name != folders_new[0].entry.name
    assert folders_new[0].entry.name == 'juancarlosfolder'
    assert b'Se ha renombrado con exito!' in res.data
    assert b'Cloud private' in res.data

def test_rename_file_public(test_client, user):
    res_file, res_folder = initialize(test_client, user, 'public')
    
    full_path = os.path.join(user.get_public_user_path(), '')
    files, folders = get_path_files_and_folders(full_path)
    file = files[0]
    
    payload = {
        'name': 'juancarlos'
    }
    
    res = test_client.post(
        '/main/cloud/rename/public/usertest/path/{0}/'.format(file.relpath),
        data=payload,
        follow_redirects=True
    )
    
    files_new, folders_new = get_path_files_and_folders(full_path)
    
    assert res.status_code == 200
    assert b'juancarlos' in res.data
    assert file.entry.name != files_new[0].entry.name
    assert files_new[0].entry.name == 'juancarlos'
    assert b'Se ha renombrado con exito!' in res.data
    assert b'Cloud public' in res.data

def test_rename_folder_public(test_client, user):
    res_file, res_folder = initialize(test_client, user, 'public')

    full_path = os.path.join(user.get_public_user_path(), '')
    files, folders = get_path_files_and_folders(full_path)
    folder = folders[0]
    
    payload = {
        'name': 'juancarlosfolder'
    }
    
    res = test_client.post(
        '/main/cloud/rename/public/usertest/path/{0}/'.format(folder.relpath),
        data=payload,
        follow_redirects=True
    )
    
    files_new, folders_new = get_path_files_and_folders(full_path)
    
    assert res.status_code == 200
    assert b'juancarlosfolder' in res.data
    assert folder.entry.name != folders_new[0].entry.name
    assert folders_new[0].entry.name == 'juancarlosfolder'
    assert b'Se ha renombrado con exito!' in res.data
    assert b'Cloud public' in res.data
    
def test_rename_folder_invalid(test_client, user, user2):
    res_file, res_folder = initialize(test_client, user, 'public')
    
    test_client.post(
        '/auth/logout'
    )
    
    test_client.post(
        '/auth/login',
        data={'email': user2.email, 'password': 'passwordtest2'}
    )
    
    full_path = os.path.join(user.get_public_user_path(), '')
    files, folders = get_path_files_and_folders(full_path)
    folder = folders[0]
    
    payload = {
        'name': 'juancarlosfolder'
    }
    
    res = test_client.post(
        '/main/cloud/rename/public/usertest/path/{0}/'.format(folder.relpath),
        data=payload,
        follow_redirects=True
    )
    
    files_new, folders_new = get_path_files_and_folders(full_path) 
    
    assert res.status_code == 404
    assert b'Not found!!' in res.data
    assert folders_new[0].entry.name == folder.entry.name
    
def test_rename_file_invalid(test_client, user, user2):
    res_file, res_folder = initialize(test_client, user, 'public')
    
    test_client.post(
        '/auth/logout'
    )
    
    test_client.post(
        '/auth/login',
        data={'email': user2.email, 'password': 'passwordtest2'}
    )
    
    full_path = os.path.join(user.get_public_user_path(), '')
    files, folders = get_path_files_and_folders(full_path)
    file = files[0]
    
    payload = {
        'name': 'juancarlos'
    }
    
    res = test_client.post(
        '/main/cloud/rename/public/usertest/path/{0}/'.format(file.relpath),
        data=payload,
        follow_redirects=True
    )
    
    files_new, folders_new = get_path_files_and_folders(full_path)
    
    assert res.status_code == 404
    assert b'Not found!!' in res.data
    assert files_new[0].entry.name == file.entry.name