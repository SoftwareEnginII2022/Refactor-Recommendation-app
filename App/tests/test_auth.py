import unittest, pytest, os
from App.main import create_app
from App.database import create_db
from App.controllers import (
    authenticate,
    create_user
)

from wsgi import app

'''
Integration Tests
'''
class AuthIntegrationTests(unittest.TestCase):

     @pytest.fixture(autouse=True, scope="class")
     def empty_db(self):
         app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
         create_db(app)
         yield app.test_client()
         os.unlink(os.getcwd()+'/App/test.db')


     def test_authenticate(self):
         user = create_user("bob", "pass", "student", "Bob","Marley")
         assert authenticate("bob", "pass") != None

