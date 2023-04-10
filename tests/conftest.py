import pytest

from .. import create_app, db
from ..config import TestingConfig
from ..models import User

@pytest.fixture()
def test_client():
    app = create_app(config_class=TestingConfig)
    
    with app.test_client() as testing_client:
        
        with app.app_context():
            db.drop_all()
            db.create_all()
            
            yield testing_client 
            
            db.session.remove()
            db.drop_all()
            
        
@pytest.fixture()
def user():
    user = User(
        username='usertest',
        email='test@test.com'
    )
    
    user.set_password('passwordtest')
    db.session.add(user)
    db.session.commit()
    
    return user

