from ...models import db, User

def test_register_page(test_client):
    res = test_client.get('/auth/register')
    
    assert res.status_code == 200
    assert b'<h1 class="h3 mb-3 fw-bold p-4">Registro</h1>'  in res.data

def test_register_user(test_client):
    payload = {
        'email': 'test@test.com',
        'username': 'testuser',
        'password': 'testpaswordd',
        'password_confirmation': 'testpaswordd'
    }
    
    res = test_client.post('/auth/register', data=payload)
    user = db.session.get(User, 1)
    
    assert res.status_code == 302
    assert user is not None
    assert user.username == 'testuser'
    
def test_register_user_invalid(test_client):
    payload = {
        'email': 'testtest.com',
        'username': 'testuser',
        'password': 'testpaswordd',
        'password_confirmation': 'tetpaswordd'
    }
    
    res = test_client.post('/auth/register', data=payload)
    
    assert b'Invalid email address.' in res.data
    assert b'Field must be equal to password.' in res.data
    
