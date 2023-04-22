def test_cloud_private_page(test_client, user):
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    res = test_client.get(
        '/main/cloud/private',
        follow_redirects=True
    )
    
    assert res.status_code == 200
    assert b'<title> Cloud private </title>' in res.data
    
def test_cloud_public_me_page(test_client, user):
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    res = test_client.get(
        '/main/cloud/public/',
        follow_redirects=True
    )
   
    assert res.status_code == 200
    assert b'<title> Cloud public </title>' in res.data
    assert user.username.encode() in res.data
    
def test_cloud_public_user_page(test_client, user, user2):
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    res = test_client.get(
        f'/main/cloud/public/{user2.username}/path/?',
        follow_redirects=True
    )
    
    assert res.status_code == 200
    assert b'<title> Cloud public </title>' in res.data
    assert user.username.encode() not in res.data
    assert b'Crear directorio' not in res.data
