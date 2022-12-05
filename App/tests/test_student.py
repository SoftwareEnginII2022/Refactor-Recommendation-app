import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import create_db
from App.models import *
from App.controllers import (
    create_user,
    get_student
)

from wsgi import app

LOGGER = logging.getLogger(__name__)

class StudentUnitTests(unittest.TestCase):
    def test_new_student(self):
        student = Student("bob@marley.com", "pass", "Bob","Marley")
        assert student.firstName == "Bob"
        assert student.lastName == "Marley"
        assert student.email == "bob@marley.com"
        assert student.getType() == "student"
        assert student.getName() == "Bob Marley"

    def test_student_toJSON(self):
        student = Student("bob@marley.com", "pass", "Bob","Marley")
        student_json = student.toJSON()
        expected_json = {
            'studentID': None,
            'email': 'bob@marley.com',
            'firstName':'Bob',
            'lastName': 'Marley',
            'requests':[]
        }
        self.assertDictEqual(student_json, expected_json)
    
    def test_hashed_password(self):
        password = "pass"
        student = Student("bob@marley.com", "pass", "Bob","Marley")
        assert student.password != password
        assert student.check_password(password)
    
    
class StudentIntegrationTests(unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def empty_db(self):
        app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        create_db(app)
        yield app.test_client()
        os.unlink(os.getcwd()+'/App/test.db')
  
    def test_create_student(self):
        student = create_user("bob@marley.com", "pass", "student", "Bob","Marley")
        view_student = get_student(student.id)
        assert view_student.id == student.id
        assert view_student.studentID == student.studentID
        assert view_student.email == student.email
        assert view_student.firstName == student.firstName
        assert view_student.lastName == student.lastName
        assert view_student.Requests == student.Requests