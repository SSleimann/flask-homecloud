from flask_login import current_user

def test_login_page(test_client):
    res = test_client.get('/auth/login')
    
    assert res.status_code == 200
    assert b'<h1 class="h3 mb-3 fw-bold p-4">Por favor inicia sesion</h1>'  in res.data
    
def test_login_user(test_client, user):
    payload = {
        'email': 'test@test.com',
        'password': 'passwordtest'
    }

    res = test_client.post(
        '/auth/login',
        data=payload
    )
    
    assert res.status_code == 302
    assert current_user == user
    
def test_login_user_invalid(test_client):
    payload = {
        'email': 'teszzxxt@test.com',
        'password': 'passwoasrdtest'
    }

    res = test_client.post(
        '/auth/login',
        data=payload
    )
    
    assert b'Email o clave invalido' in res.data 
    
