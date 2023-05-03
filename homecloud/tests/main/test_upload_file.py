import os
import io

def test_upload_private_file(test_client, user):
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    file = io.BytesIO(b"testing")
    
    payload = {
        'file': (file, 'test.txt'),
        'next': '/main/cloud/private',
    }
    
    res = test_client.post(
        '/main/cloud/upload_file/private/usertest/path/',
        data=payload,
        follow_redirects=True
    )
    
    full_path = os.path.join(user.get_private_user_path(), 'test.txt')
    
    assert b'test.txt' in res.data
    assert 200 == res.status_code
    assert b'<title> Cloud private </title>' in res.data
    assert os.path.isfile(full_path) == True
    
def test_upload_public_file(test_client, user):
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    file = io.BytesIO(b"testing")
    
    payload = {
        'file': (file, 'test2.txt'),
        'next': '/main/cloud/public',
    }
    
    res = test_client.post(
        '/main/cloud/upload_file/public/usertest/path/',
        data=payload,
        follow_redirects=True
    )
    
    full_path = os.path.join(user.get_public_user_path(), 'test2.txt')
    
    assert b'test2.txt' in res.data
    assert 200 == res.status_code
    assert b'<title> Cloud public </title>' in res.data
    assert os.path.isfile(full_path) == True

def test_upload_public_invalid_file(test_client, user, user2):
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    file = io.BytesIO(b"testing")
    
    payload = {
        'file': (file, 'test3.txt'),
        'next': '/main/cloud/public',
    }
    
    res = test_client.post(
        '/main/cloud/upload_file/public/usertest2/path/',
        data=payload,
        follow_redirects=True
    )
    
    user_path = user.get_public_user_path()
    full_path = os.path.join(user_path, 'test3.txt')
    
    assert b'test3.txt' not in res.data
    assert 404 == res.status_code
    assert os.path.isfile(full_path) == False
    assert b'Not found!!' in res.data