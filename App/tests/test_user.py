import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import create_db
from App.models import *
from App.controllers import (
    create_user,
    get_user,
    get_user_by_email
)

from wsgi import app

LOGGER = logging.getLogger(__name__)

class UserUnitTests(unittest.TestCase):
    def test_new_user(self):
        user = User("bob@marley.com", "pass", "Bob","Marley")
        assert user.firstName == "Bob"
        assert user.lastName == "Marley"
        assert user.email == "bob@marley.com"
        assert user.getType() == "user"
        assert user.getName() == "Bob Marley"

    def test_user_toJSON(self):
        user = User("bob@marley.com", "pass", "Bob","Marley")
        user_json = user.toJSON()
        expected_json = {
            'id': None,
            'email': 'bob@marley.com',
            'firstName':'Bob',
            'lastName': 'Marley',
        }
        self.assertDictEqual(user_json, expected_json)
    
    def test_hashed_password(self):
        password = "pass"
        user = User("bob@marley.com", "pass", "Bob","Marley")
        assert user.password != password
        assert user.check_password(password)
    
    
class UserIntegrationTests(unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def empty_db(self):
        app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        create_db(app)
        yield app.test_client()
        os.unlink(os.getcwd()+'/App/test.db')
  
    def test_create_user(self):
        user = create_user("bob@marley.com", "pass", "user", "Bob","Marley")
        view_user = get_user(user.id)
        assert view_user.id == user.id
        assert view_user.email == user.email
        assert view_user.firstName == user.firstName
        assert view_user.lastName == user.lastName
  
    def test_get_user_by_email(self):
        user = create_user("keanu@reeves.com", "pass", "user", "Keanu","Reeves")
        view_user = get_user_by_email("keanu@reeves.com")
        assert view_user.id == user.id
        assert view_user.email == user.email
        assert view_user.firstName == user.firstName
        assert view_user.lastName == user.lastName