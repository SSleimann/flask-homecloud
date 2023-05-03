import os

def test_create_private_directory(test_client, user):
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    payload = {
        'next': '/main/cloud/private',
        'dir': 'testFolder'
    }
    
    res = test_client.post(
        '/main/cloud/create_dir/private/usertest/path/',
        data=payload,
        follow_redirects=True
    )
    
    full_path = os.path.join(user.get_private_user_path(), 'testFolder', '')
    
    assert res.status_code == 200
    assert b'testFolder' in res.data
    assert b'<title> Cloud private </title>' in res.data
    assert os.path.exists(full_path) == True

def test_create_public_directory(test_client, user):
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    payload = {
        'next': '/main/cloud/public',
        'dir': 'testFolder'
    }
    
    res = test_client.post(
        '/main/cloud/create_dir/public/usertest/path/',
        data=payload,
        follow_redirects=True
    )
    
    full_path = os.path.join(user.get_public_user_path(), 'testFolder', '')
    
    assert res.status_code == 200
    assert b'testFolder' in res.data
    assert b'<title> Cloud public </title>' in res.data
    assert os.path.exists(full_path) == True

def test_create_user_invalid_directory(test_client, user, user2):
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    payload = {
        'next': '/main/cloud/public',
        'dir': 'testFolder'
    }
    
    res = test_client.post(
        '/main/cloud/create_dir/public/usertest2/path/',
        data=payload
    )
    
    full_path = os.path.join(user.get_public_user_path(), 'testFolder', '')
    
    assert b'Not found!!' in res.data
    assert res.status_code == 404
    assert b'testFolder' not in res.data
    assert os.path.exists(full_path) == False