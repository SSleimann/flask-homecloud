import os
import io
import typing as t

from homecloud.utils import get_path_files_and_folders
from homecloud.models import User

T = t.TypeVar('T')

def initialize(test_client, user: User, state: t.Literal['private', 'public']) -> T:
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    file = io.BytesIO(b"testing")
    payload = {
        'file': (file, 'test.txt'),
        'next': '/main/cloud/{0}'.format(state),
    }
    
    res = test_client.post(
        '/main/cloud/upload_file/{0}/usertest/path/'.format(state),
        data=payload,
        follow_redirects=True
    )
    
    return res
    
def test_delete_private_file(test_client, user):
    res_init = initialize(test_client, user, 'private')
    
    full_path = os.path.join(user.get_private_user_path(), '')
    files_old, _ = get_path_files_and_folders(full_path)
    file_relpath = files_old[0].relpath
    
    res_del = test_client.post(
        '/main/cloud/delete_file/private/usertest/path/{0}/'.format(file_relpath),
        follow_redirects=True
    )
    
    files_new, _ = get_path_files_and_folders(full_path)
    
    assert len(files_old) == 1
    assert len(files_new) == 0
    assert b'Se ha eliminado con exito el archivo' in res_del.data
    assert res_del.status_code == 200
    assert b'Cloud private' in res_del.data

def test_delete_public_file(test_client, user):
    res_init = initialize(test_client, user, 'public')
    
    full_path = os.path.join(user.get_public_user_path(), '')
    files_old, _ = get_path_files_and_folders(full_path)
    file_relpath = files_old[0].relpath
    
    res_del = test_client.post(
        '/main/cloud/delete_file/public/usertest/path/{0}/'.format(file_relpath),
        follow_redirects=True
    )
    
    files_new, _ = get_path_files_and_folders(full_path)
    
    assert b'test.txt' in res_init.data
    assert len(files_old) == 1
    assert len(files_new) == 0
    assert b'Se ha eliminado con exito el archivo' in res_del.data
    assert res_del.status_code == 200
    assert b'Cloud public' in res_del.data
    
def test_delete_invalid_file(test_client, user, user2):
    res_init = initialize(test_client, user, 'public')
    
    test_client.post(
        '/auth/logout'
    )
    
    test_client.post(
        '/auth/login',
        data={'email': user2.email, 'password': 'passwordtest2'}
    )
    
    user1_path = os.path.join(user.get_public_user_path(), '')
    files_old, _ = get_path_files_and_folders(user1_path)
    file_relpath = files_old[0].relpath
    
    res_del = test_client.post(
        '/main/cloud/delete_file/public/usertest/path/{0}/'.format(file_relpath),
        follow_redirects=True
    )

    files_new, _ = get_path_files_and_folders(user1_path)
    
    assert res_del.status_code == 404
    assert b'Not found!!' in res_del.data
    assert len(files_new) == 1
    assert len(files_old) == 1
    
