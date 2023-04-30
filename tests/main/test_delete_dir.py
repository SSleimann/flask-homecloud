import os
import io
import typing as t

from ...utils import get_path_files_and_folders
from ...models import User

T = t.TypeVar('T')

def initialize(test_client, user: User, state: t.Literal['private', 'public']) -> T:
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    payload = {
        'next': '/main/cloud/{}'.format(state),
        'dir': 'testFolder'
    }
    
    res = test_client.post(
        '/main/cloud/create_dir/{0}/usertest/path/'.format(state),
        data=payload,
        follow_redirects=True
    )
    
    return res

def test_delete_public_dir(test_client, user):
    init = initialize(test_client, user, 'public')
    
    user_path = os.path.join(user.get_public_user_path(), '')
    files_old, folders_old = get_path_files_and_folders(user_path)
    folder = folders_old[0]
    
    res_del = test_client.post(
        '/main/cloud/delete_file/public/usertest/path/{0}/'.format(folder.relpath),
        follow_redirects=True
    )
    
    files_old, folders_new = get_path_files_and_folders(user_path)
    
    assert folders_new == []
    assert len(folders_old) == 1
    assert b'Cloud public' in res_del.data
    assert b'Se ha eliminado con exito la carpeta!' in res_del.data
    assert b'testFolder' not in res_del.data
    assert res_del.status_code == 200
    assert b'testFolder' in init.data
    
def test_delete_private_dir(test_client, user):
    init = initialize(test_client, user, 'private')
    
    user_path = os.path.join(user.get_private_user_path(), '')
    files_old, folders_old = get_path_files_and_folders(user_path)
    folder = folders_old[0]
    
    res_del = test_client.post(
        '/main/cloud/delete_file/private/usertest/path/{0}/'.format(folder.relpath),
        follow_redirects=True
    )
    
    files_old, folders_new = get_path_files_and_folders(user_path)
    
    assert folders_new == []
    assert len(folders_old) == 1
    assert b'Cloud private' in res_del.data
    assert b'Se ha eliminado con exito la carpeta!' in res_del.data
    assert b'testFolder' not in res_del.data
    assert res_del.status_code == 200
    assert b'testFolder' in init.data

def test_delete_invalid_dir(test_client, user, user2):
    init = initialize(test_client, user, 'public')
    
    test_client.post(
        '/auth/logout'
    )
    
    test_client.post(
        '/auth/login',
        data={'email': user2.email, 'password': 'passwordtest2'}
    )
    
    user_path = os.path.join(user.get_public_user_path(), '')
    files_old, folders_old = get_path_files_and_folders(user_path)
    folder = folders_old[0]
    
    res_del = test_client.post(
        '/main/cloud/delete_file/public/usertest/path/{0}/'.format(folder.relpath),
        follow_redirects=True
    )
    
    files_new, folders_new = get_path_files_and_folders(user_path)
    
    assert res_del.status_code == 404
    assert len(folders_old) == 1
    assert len(folders_new) == 1
    assert b'testFolder' in init.data
    assert b'Not found!!' in res_del.data
    