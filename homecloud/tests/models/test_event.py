from homecloud.models import db, User

def test_lower_event(test_client):
    user = User(
        username='SleimanPrueba1',
        email= 'sleimanprueba@email.com'
    )
    user.set_password('pruebaextrema')
    db.session.add(user)
    db.session.commit()
    
    find_user = db.session.get(User, 1)
    
    assert find_user is not None
    assert find_user.username.islower() is True
    assert find_user.username == 'sleimanprueba1'
    
