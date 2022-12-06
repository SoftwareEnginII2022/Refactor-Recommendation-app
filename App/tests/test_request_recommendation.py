import os, tempfile, pytest, logging, unittest

from datetime import datetime, timedelta
from App.main import create_app
from App.database import create_db
from App.models import Status
from App.models import *
from App.controllers import (
    create_request,
    get_request,
    get_student_requests,
    accept_request,
    reject_request,
    cancel_request
)

from wsgi import app

LOGGER = logging.getLogger(__name__)

class Request_RecommendationUnitTests(unittest.TestCase):
    def test_new_request_recommendation(self):
        deadline = datetime.now() + timedelta(days=5)
        req_rec = Request_Recommendation(0, 1, deadline, "Recommendation Please")
        assert req_rec.staffID == 0
        assert req_rec.studentID == 1
        assert req_rec.deadline == deadline
        assert req_rec.requestBody == "Recommendation Please"
        assert req_rec.status == Status.PENDING

    def test_request_recommendation_toJSON(self):
        deadline = datetime.now() + timedelta(days=5)
        req_rec = Request_Recommendation(0, 1, deadline, "Recommendation Please")
        req_rec_json = req_rec.toJSON()
        req_rec_json.pop("dateRequested")
        expected_json = {
            'reqID': None,
            'staffID': 0,
            'studentID': 1,
            'deadline': deadline,
            'status': Status.PENDING.value,
            'requestBody': "Recommendation Please",
            'recommendation': None
        }
        self.assertDictEqual(req_rec_json, expected_json)
    
    
class Request_RecommendationIntegrationTests(unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def empty_db(self):
        app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        create_db(app)
        yield app.test_client()
        os.unlink(os.getcwd()+'/App/test.db')
  
    def test_create_request(self):
        deadline = datetime.now() + timedelta(days=5)
        req_rec = create_request(0, 1, deadline, "Recommendation Please")
        view_req_rec = get_request(req_rec.reqID)
        assert view_req_rec.staffID == req_rec.staffID
        assert view_req_rec.studentID == req_rec.studentID
        assert view_req_rec.deadline == req_rec.deadline
        assert view_req_rec.dateRequested == req_rec.dateRequested
        assert view_req_rec.requestBody == req_rec.requestBody
        assert view_req_rec.status == req_rec.status
        assert view_req_rec.Recommendation == req_rec.Recommendation
  
    def test_create_request_stu_dent(self):
        deadline = datetime.now() + timedelta(days=5)
        req_rec = create_request(0, 2, deadline, "Recommendation Please")
        [view_req_rec] = get_student_requests(req_rec.studentID)
        assert view_req_rec.staffID == req_rec.staffID
        assert view_req_rec.studentID == req_rec.studentID
        assert view_req_rec.deadline == req_rec.deadline
        assert view_req_rec.dateRequested == req_rec.dateRequested
        assert view_req_rec.requestBody == req_rec.requestBody
        assert view_req_rec.status == req_rec.status
        assert view_req_rec.Recommendation == req_rec.Recommendation
  
    def test_accept_request(self):
        deadline = datetime.now() + timedelta(days=5)
        req_rec = create_request(0, 3, deadline, "Recommendation Please")
        view_req_rec = get_request(req_rec.reqID)
        assert view_req_rec.status == Status.PENDING
        
        accept_request(req_rec.reqID)
        assert view_req_rec.status == Status.ACCEPTED
  
    def test_reject_request(self):
        deadline = datetime.now() + timedelta(days=5)
        req_rec = create_request(0, 4, deadline, "Recommendation Please")
        view_req_rec = get_request(req_rec.reqID)
        assert view_req_rec.status == Status.PENDING
        
        reject_request(req_rec.reqID)
        assert view_req_rec.status == Status.REJECTED
  
    def test_cancel_request(self):
        deadline = datetime.now() + timedelta(days=5)
        req_rec = create_request(0, 5, deadline, "Recommendation Please")
        view_req_rec = get_request(req_rec.reqID)
        assert view_req_rec.status == Status.PENDING
        
        cancel_request(req_rec.reqID)
        assert view_req_rec.status == Status.CANCELLED