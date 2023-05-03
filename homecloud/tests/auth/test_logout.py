from flask_login import current_user, AnonymousUserMixin

def test_logout_page(test_client, user):
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    res = test_client.get(
        '/auth/logout',
    )
    
    assert b'Quieres salir de la sesion?' in res.data
    assert b'_logout' in res.data

def test_logout_user(test_client, user):
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    res = test_client.post(
        '/auth/logout',
    )

    assert res.status_code == 302
    assert isinstance(current_user, AnonymousUserMixin) == True
    
def test_logout_user_invalid(test_client, user):
    test_client.post(
        '/auth/login',
        data={'email': user.email, 'password': 'passwordtest'}
    )
    
    res = test_client.post(
        '/auth/logout',
        data={'logout': '123'}
    )
    
    assert b'Quieres salir de la sesion?' in res.data

