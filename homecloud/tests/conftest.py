import pytest
import shutil

from homecloud.app import create_app, db
from homecloud.config import TestingConfig
from homecloud.models import User

@pytest.fixture()
def test_client():
    app = create_app(config_class=TestingConfig)
    UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
     
    with app.test_client() as testing_client:
        
        with app.app_context():
            db.drop_all()
            db.create_all()
            
            yield testing_client 
            
            db.session.remove()
            db.drop_all()
            
            shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
        
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

@pytest.fixture()
def user2():
    user = User(
        username='usertest2',
        email='test2@test.com'
    )
    
    user.set_password('passwordtest2')
    db.session.add(user)
    db.session.commit()
    
    return user

