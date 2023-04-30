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

def test_download_private_file(test_client, user):
    initialize(test_client, user, 'private')
    
    user_path = os.path.join(user.get_private_user_path(), '')
    files, _ = get_path_files_and_folders(user_path)
    file_relpath = files[0].relpath
    
    res = test_client.get(
        '/main/cloud/download_file/private/usertest/path/{0}'.format(file_relpath)
    )
    
    assert res.headers['Content-Disposition'] == 'attachment; filename=test.txt'
    assert res.data == b"testing"
    assert res.status_code == 200

def test_download_public_file(test_client, user):
    initialize(test_client, user, 'public')
    
    user_path = os.path.join(user.get_public_user_path(), '')
    files, _ = get_path_files_and_folders(user_path)
    file_relpath = files[0].relpath
    
    res = test_client.get(
        '/main/cloud/download_file/public/usertest/path/{0}'.format(file_relpath)
    )
    
    assert res.headers['Content-Disposition'] == 'attachment; filename=test.txt'
    assert res.data == b"testing"
    assert res.status_code == 200

def test_download_private_not_exist_file(test_client, user):
    initialize(test_client, user, 'private')
    
    res = test_client.get(
        '/main/cloud/download_file/private/usertest/path/test.txt'
    )
    
    assert b'404 Not Found' in res.data
    assert b"testing" not in res.data
    assert res.status_code == 404
    
def test_download_public_not_exist_file(test_client, user):
    initialize(test_client, user, 'public')
    
    res = test_client.get(
        '/main/cloud/download_file/public/usertest/path/test.txt'
    )
    
    assert b'404 Not Found' in res.data
    assert b"testing" not in res.data
    assert res.status_code == 404
    
def test_download_private_file_invalid(test_client, user, user2):
    initialize(test_client, user, 'private')
    
    test_client.post(
        '/auth/logout'
    )
    
    test_client.post(
        '/auth/login',
        data={'email': user2.email, 'password': 'passwordtest2'}
    )
    
    user_path = os.path.join(user.get_private_user_path(), '')
    files, _ = get_path_files_and_folders(user_path)
    file_relpath = files[0].relpath
    
    res = test_client.get(
        '/main/cloud/download_file/private/usertest/path/{0}'.format(file_relpath)
    )
    
    assert res.status_code == 404
    assert b'Este archivo no existe' in res.data
    