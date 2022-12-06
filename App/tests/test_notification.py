import os, tempfile, pytest, logging, unittest

from datetime import datetime, timedelta
from App.main import create_app
from App.database import create_db
from App.models import Status
from App.models import *
from App.controllers import (
    create_request,
    set_notification_seen,
    get_notification_by_request
)

from wsgi import app

LOGGER = logging.getLogger(__name__)

class NotificationUnitTests(unittest.TestCase):
    def test_new_notification(self):
        notif = Notification(0, 1)
        assert notif.reqID == 0
        assert notif.staffID == 1
        assert notif.seen == False

    def test_notification_toJSON(self):
        notif = Notification(0, 1)
        notif_json = notif.toJSON()
        notif_json.pop("timestamp")
        expected_json = {
            'notificationID': None,
            'reqID': 0,
            'staffID': 1,
            'request': None,
            'seen': False,
        }
        self.assertDictEqual(notif_json, expected_json)
    
    
class NotificationIntegrationTests(unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def empty_db(self):
        app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        create_db(app)
        yield app.test_client()
        os.unlink(os.getcwd()+'/App/test.db')
  
    def test_create_notification(self):
        deadline = datetime.now() + timedelta(days=5)
        req_rec = create_request(0, 9, deadline, "Recommendation Please")
        view_notif = get_notification_by_request(req_rec.reqID)
        assert view_notif.reqID == req_rec.reqID
        assert view_notif.staffID == req_rec.staffID
        assert view_notif.seen == False
        assert view_notif.Request_Recommendation == req_rec
  
    def test_set_notification_true(self):
        deadline = datetime.now() + timedelta(days=5)
        req_rec = create_request(0, 10, deadline, "Recommendation Please")
        view_notif = get_notification_by_request(req_rec.reqID)
        
        assert view_notif.seen == False
        
        set_notification_seen(view_notif)
        
        
        view_notif = get_notification_by_request(req_rec.reqID)
        assert view_notif.seen == True