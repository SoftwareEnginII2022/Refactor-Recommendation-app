import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import create_db
from App.models import *
from App.controllers import (
    create_user,
    get_staff,
    get_staff_names
)

from wsgi import app

LOGGER = logging.getLogger(__name__)

class StaffUnitTests(unittest.TestCase):
    def test_new_staff(self):
        staff = Staff("bob@marley.com", "pass", "Bob","Marley")
        assert staff.firstName == "Bob"
        assert staff.lastName == "Marley"
        assert staff.email == "bob@marley.com"
        assert staff.getType() == "staff"
        assert staff.getName() == "Bob Marley"

    def test_staff_toJSON(self):
        staff = Staff("bob@marley.com", "pass", "Bob","Marley")
        staff_json = staff.toJSON()
        expected_json = {
            'staffID': None,
            'email': 'bob@marley.com',
            'firstName':'Bob',
            'lastName': 'Marley',
            'notifications':[]
        }
        self.assertDictEqual(staff_json, expected_json)
    
    def test_hashed_password(self):
        password = "pass"
        staff = Staff("bob@marley.com", "pass", "Bob","Marley")
        assert staff.password != password
        assert staff.check_password(password)
    
    
class StaffIntegrationTests(unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def empty_db(self):
        app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        create_db(app)
        yield app.test_client()
        os.unlink(os.getcwd()+'/App/test.db')
  
    def test_create_staff(self):
        staff = create_user("mister@mendez.com", "pass", "staff", "Mister","Mendez")
        view_staff = get_staff(staff.staffID)
        assert view_staff.id == staff.id
        assert view_staff.staffID == staff.staffID
        assert view_staff.email == staff.email
        assert view_staff.firstName == staff.firstName
        assert view_staff.lastName == staff.lastName
        assert view_staff.Notification == staff.Notification
  
    def test_get_staff_names(self):
        staff = create_user("doctor@mendez.com", "pass", "staff", "Doctor","Mendez")
        [a, view_staff, *z] = get_staff_names()
        print(view_staff)
        assert "id" not in view_staff
        assert view_staff.staffID == staff.staffID
        assert "email" not in view_staff
        assert view_staff.firstName == staff.firstName
        assert view_staff.lastName == staff.lastName
        assert "Notification" not in view_staff